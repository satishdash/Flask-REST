#!/bin/bash

##################################################################################################
# 
# A flask application server with defined web routes.
# [ REST based recruiter data store system]
#
# @author : Satish Dash
#
##################################################################################################

import json
import os
import sys
import uuid
from threading import RLock
import uuid
from flask import Flask, jsonify, request

from error import Error

import httpstatus
from db.dbconnect import MongoDB
from exceptions.exception import CandidateException , ExperienceException, ProjectException
from models.candidate import Candidate
from models.experience import Experience

# app variable to run this as a flask application
app = Flask(__name__)


# route: GET /
@app.route("/")
@app.route("/home")
def root():
	d = {"message": "Welcome! This is a flask web server"}
	return jsonify(d)


# route: POST /add-candidate
@app.route("/add-candidate", methods=["POST","GET"])
def addCandidate():
	if request.method == "POST":
		# get json body sent in the request, comes as a dict.
		body = request.get_json(force=True)

		print("Request body: " , body, file=sys.stdout)
		print(type(body), file=sys.stdout)

		response = {"message" : None}
		# send body for validation
		try:
			candidate = Candidate(json.dumps(body))
			if candidate.isProfileValid():
				# store in DB
				mongodb = MongoDB()
				candidateCol = mongodb.getCollection()
				lock = RLock()
				auto = str(uuid.uuid4().int >>64)
				with lock:
					if candidateCol.count({"_id":auto}) > 0:
						auto = str(uuid.uuid4().int >> 64)
				body["_id"] = str(auto)
				candidateCol.insert_one(body)
				response["message"] = "Requested profile is successfully added to the candidate entitlement."
				response["candidate_id"] = auto
			else:
				response["message"] = "Profile seems to be invalid. Needs correction(s). Please resend a valid profile."
		except (CandidateException, ExperienceException, ProjectException) as exp:
			err = Error(exp.args[0], httpstatus.BAD_REQUEST)
			return jsonify(err.serialize()), httpstatus.BAD_REQUEST
		except Exception as exp:
			#err = Error("Internal server error has occurred.", httpstatus.SERVER_ERROR)
			err = Error(exp.args[0], httpstatus.SERVER_ERROR)
			return jsonify(err.serialize()), httpstatus.SERVER_ERROR
			
		return jsonify(response), httpstatus.SUCCESS
	elif request.method == "GET":
		return jsonify(json.loads(open("sample.json").read())), httpstatus.SUCCESS

# route: GET /get-all-candidates
@app.route("/get-all-candidates")
def getAllCandidates():
	response = {"message":{"items":None}}
	candidates = []
	try:
		mongodb = MongoDB()
		candidateCol = mongodb.getCollection()

		# fetch all candidates from DB
		cur = candidateCol.find().sort([("_id", 1)])
		for c in cur:
			candidates.append(c)
		response["message"]["items"] = candidates
	except Exception as e:
		err = Error(e.args[0] + ": Internal server error has occurred.", httpstatus.SERVER_ERROR)
		return jsonify(err.serialize()), httpstatus.SERVER_ERROR
	else:
		return jsonify(response), httpstatus.SUCCESS

# route: GET /get-candidate?<string:candidate Name>&<string:domain>&<string:years>


# route: POST /add-candidate-experience/<string: id>
@app.route("/edit-candidate-experience", methods=["POST"])
def editCandidateExperience():
	response = {"message":None}
	status = httpstatus.NOT_FOUND
	try:
		body = request.get_json(force=True)
		if body:
			pass
		else:
			status = httpstatus.BAD_REQUEST
			response["message"] = "JSON payload is missing from the request. Please provide an appropriate"\
			+ " experience list to be updated for the profile."
			return jsonify(response) , status
		if request.args.get("id"):
			_id = request.args.get("id")
			mongodb = MongoDB()
			candidateCol = mongodb.getCollection()
			if candidateCol.count({"_id":_id}) > 0:
				e = Experience(json.dumps(body))
				if e.isExperienceValid():
					res = candidateCol.update_one({"_id": _id}, {"$set":{"experience":body}})
					status = httpstatus.SUCCESS
					response["message"] = "Experience list for candidate profile with"\
					+ " id '{}' updated successfully.".format(_id)
			else:
				status = httpstatus.NOT_FOUND
				response["message"] = "Candidate profile with id '{}' not found.".format(_id)\
				+ " Please provide a valid candidate profile ID."

		else:
			status = httpstatus.BAD_REQUEST
			response["message"] = "'id' not available as a request parameter. "\
			+ "Please provide a valid 'id' for modification."
		
	except ExperienceException as ee:
		status = httpstatus.BAD_REQUEST
		err= Error(ee.args[0], status)
		return jsonify(err.serialize()), status
	except Exception as exp:
		status = httpstatus.SERVER_ERROR
		err= Error(str(exp.args) + ":" + " Internal server error has occurred.", httpstatus.SERVER_ERROR)
		return jsonify(err.serialize()), status
	else:
		return jsonify(response), status



# route: DELETE /remove-candidate?<string:id>
@app.route("/remove-candidate", methods=["DELETE"])
def removeCandidate():
	response = {"message":None}
	status = httpstatus.NOT_FOUND
	try:
		# validate if args is present
		if request.args.get("id"):
			_id = request.args.get("id")
			mongodb = MongoDB()
			candidateCol = mongodb.getCollection()
			# remove the candidate
			res = candidateCol.delete_one({"_id":_id})
			if res.deleted_count > 0:
				status = httpstatus.SUCCESS
				response["message"] = "Candidate profile with ID '{}' is successfully removed from the entitlement."\
				.format(_id)
			else:
				response["message"] = "Candidate profile with ID '{}' could not be found.".format(_id)\
				+ " Please provide a valid candidate profile ID."
		else:
			status = httpstatus.BAD_REQUEST
			response["message"] = "'id' as request parameter is missing. Please pass a valid candidate 'id' for removal."

	except Exception as e:
		err = Error(e.args[0] + ":" + "Internal server error has occurred.", httpstatus.SERVER_ERROR)
		return jsonify(err.serialize()), httpstatus.SERVER_ERROR
	else:
		return jsonify(response), status

if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=5000)

