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
from flask import Flask, jsonify, request

from error import Error

import httpstatus
from db.dbconnect import MongoDB
from exceptions.exception import CandidateException , ExperienceException, ProjectException
from models.candidate import Candidate

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
				auto = 0
				with lock:
					auto = candidateCol.count()
					auto += 1
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


# route: GET /get-candidate?<string:candidate Name>&<string:domain>&<string:years>


# route: POST /edit-candidate-experience/<int:candidate ID>


# route: DELETE /remove-candidate/<int:candidate ID>

if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=5000)

