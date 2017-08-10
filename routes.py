#!/bin/bash

##################################################################################################
# 
# A flask application server with defined web routes.
# [ REST based recruiter data store application ]
#
# @author : Satish Dash
#
##################################################################################################

import json
import os
import random
import sys
import uuid
from flask import Flask, jsonify, request, url_for

import httpstatus
from credential import Credential
from db.dbconnect import MongoDB
from error import Error
from exceptions.exception import CandidateException , ExperienceException, ProjectException
from models.candidate import Candidate
from models.experience import Experience

# App variable to run this as a flask application
app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

# route: GET /
@app.route("/")
@app.route("/home")
def root():
	d = {"message": "Welcome! This is a (python) FLASK web server."}
	return jsonify(d)


# route: POST /add-candidate
@app.route("/add-candidate", methods=["POST","GET"])
def addCandidate():
	resp = tokenValidator(request.args.get("token", None))
	if resp:
		return jsonify(resp[0]), resp[1]
	if request.method == "POST":
		# get json body sent in the request, comes as a dict.
		body = request.get_json(force=True)

		print("Request body: " , body, file=sys.stdout)
		# Send body for validation
		try:
			candidate = Candidate(json.dumps(body))
			if candidate.isProfileValid():
				# store in DB
				mongodb = MongoDB()
				candidateCol = mongodb.getCollection()
				auto = str(uuid.uuid4().int >>64)
				if candidateCol.count({"_id":auto}) > 0:
					auto = str(uuid.uuid4().int >> 64)
				body["_id"] = str(auto)
				candidateCol.insert_one(body)
				response["message"] = "Requested profile is SUCCESSFULLY added to the candidate entitlement."
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
	response = {"message":None}
	candidates = []
	resp = tokenValidator(request.args.get("token", None))
	if resp:
		return jsonify(resp[0]), resp[1]
	try:
		mongodb = MongoDB()
		candidateCol = mongodb.getCollection()

		# fetch all candidates from DB
		cur = candidateCol.find().sort([("_id", 1)])
		for c in cur:
			candidates.append(c)
		response["items"] = candidates
		response["message"] = "List of candidate profiles in the entitlement."
	except Exception as e:
		err = Error(e.args[0] + ": Internal server error has occurred.", httpstatus.SERVER_ERROR)
		return jsonify(err.serialize()), httpstatus.SERVER_ERROR
	else:
		return jsonify(response), httpstatus.SUCCESS


# route: GET /get-candidate?<string:candidate Name>&<string:domain>&<string:years>
@app.route("/get-candidate")
def getCandidate():
	response = {"message" : None}
	status = httpstatus.NOT_FOUND
	name =  request.args.get("name", None)
	domain =  request.args.get("domain", None)
	years = request.args.get("years", None)
	total_years = request.args.get("total-exp", None)

	resp = tokenValidator(request.args.get("token", None))
	if resp:
		return jsonify(resp[0]), resp[1]

	# Check if any of these filters are provided
	if name or domain or years or total_years:
		pass
	else:
		status = httpstatus.BAD_REQUEST
		response["message"] = "Please pass in appropriate candidate filters for obtaining information."\
		+" Allowed filters are: 'name', <'domain', 'years'>, "\
		+ "'total-exp.'"\
		+ "['years', 'total-exp' will be checked for a greater than or an equal to match ONLY],"\
		+ "['domain', 'years' must be passed together if so passed as filter. Either one is not allowed.]"
		return jsonify(response), status

	# Collect the parameter values
	query = []
	mongodb = None
	if name:
		query.append({"name" : {"$regex":"^" +name.strip()+ "$", "$options":"i"}})
		print(query)
	if domain or years:
		if domain and years:
			pass
		else:
			status = httpstatus.BAD_REQUEST
			response["message"] = "<domain> and <years> filter(s) must be passed together."
			return jsonify(response), status
		domain = domain.strip()
		years = years.strip()
		try:
			y = float(years)
		except:
			status = httpstatus.BAD_REQUEST
			response["message"] = "Years mentioned is in incorrect format, Value passed"\
			+ "={}. Must be a number.".format(years)
			return jsonify(response), status
		else:
			query.append({"experience" : {"$elemMatch" : {"domain": {"$regex":"^"+domain + "$", "$options":"i"}\
				, "years":{"$gte":float(years)}}}})
			print(query)
	
	if total_years:
		total_years = total_years.strip()
		try:
			total = float(total_years)
		except:
			status = httpstatus.BAD_REQUEST
			response["message"] = "Total years of experience mentioned is in incorrect format, Value passed"\
			+ "={}. Must be a number".format(total_years)
			return jsonify(response), status
		else:
			idList = []
			try:
				mongodb = MongoDB()
				candidateCol = mongodb.getCollection()
				q = [{"$unwind":"$experience"}\
					,{"$group" : {"_id":"$_id", "total":{"$sum":"$experience.years"}}}\
					,{"$match":{"total":{"$gte":float(total_years)}}}\
					, {"$project":{"_id":1}}\
					]
				idList = list(candidateCol.aggregate(q))
				idList = [doc["_id"] for doc in idList]
				print(idList)
			except Exception as e:
				status = httpstatus.SERVER_ERROR
				response["message"] = str(e.args) + ":" + " Internal server error has occurred."
				return jsonify(response), status
			else:
				if idList:
					query.append({"_id":{"$in":idList}})
					print(query)
				else:
					status = httpstatus.NOT_FOUND
					response["message"] = "No such candidate profile exists where total experience is"\
					" greater than or equal to {} years.".format(total_years)
					return jsonify(response), status

	# Indicates there is a query to be executed.
	cur = None
	try:
		mongodb = MongoDB()
		candidateCol = mongodb.getCollection()
		cur = candidateCol.find({"$and":query})
	except Exception as e:
		status = httpstatus.SERVER_ERROR
		response["message"] = str(e.args) + ":" + " Internal server error."
	if cur:
		response["items"] = []
		for c in cur:
			response["items"].append(c)
		if response["items"]:
			status = httpstatus.SUCCESS
			response["message"] = "Candidate profiles SUCCESSFULLY retrieved as requested."
		else:
			response.pop("items")
			status - httpstatus.NOT_FOUND
			response["message"] = "Candidate profiles don't exist for the applied filters."
	else:
		status - httpstatus.NOT_FOUND
		response["message"] = "Candidate profiles don't exist for the applied filters."
	return jsonify(response), status



# route: POST /add-candidate-experience/<string: id>
@app.route("/edit-candidate-experience", methods=["POST"])
def editCandidateExperience():
	response = {"message":None}
	status = httpstatus.NOT_FOUND

	resp = tokenValidator(request.args.get("token", None))
	if resp:
		return jsonify(resp[0]), resp[1]
	try:
		body = request.get_json(force=True, silent=True)
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
		
	except (ExperienceException, ProjectException) as ee:
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
	resp = tokenValidator(request.args.get("token", None))
	if resp:
		return jsonify(resp[0]), resp[1]
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


# route GET /list-apis. Lists all API's in this server
@app.route("/list-apis")
def listApis():
	response = {"message": "List of REST end-points available in the server."}
	response["items"] = []
	response["items"].append({"add-candidate" : url_for('addCandidate') })
	response["items"].append({"get-all-candidates" : url_for('getAllCandidates') })
	response["items"].append({"get-candidate" : url_for('getCandidate') })
	response["items"].append({"remove-candidate" : url_for('removeCandidate') })
	response["items"].append({"edit-candidate-experience" : url_for('editCandidateExperience') })
	response["items"].append({"list-apis" : url_for('listApis') })
	response["items"].append({"auth" : url_for('authenticate')})
	return jsonify(response), httpstatus.SUCCESS

# route POST /auth . Authencticate to get a token for a given username/password
@app.route("/auth", methods=["POST"])
def authenticate():
	status = httpstatus.SUCCESS
	response = {"message":None}
	response["message"] = "Username and password are successfully validated. "\
	"Please use the token for future API requests."
	creds = request.headers.get("Authorization")
	try:
		if creds:
			cr = Credential(creds)
			if cr.isValid():
				status = httpstatus.SUCCESS
				response["message"] = "Authentication successfull !!!"
				response["token"] = cr.getToken()
				response["expiry-time-in-UTC"] = str(cr.getExpiryTime())
				# Store the username in the sessions object to aid token based authentication
				# for the cached user at one time.
				print("Current user in session: " , cr.getUserName())
			else:
				status = httpstatus.UNAUTHORIZED
				response["message"] = "Invalid credentials passed in the request. "\
				"Please pass a valid credential base64 (UTF-8) encoded."
		else:
			status = httpstatus.BAD_REQUEST
			response["message"] = "Basic authentication credentials are missing from the request. "\
			"Please pass a valid base64 (UTF-8) encoded username:password in the 'Authorization' header."
	except Exception as e:
		print(e.args)
		status = httpstatus.SERVER_ERROR
		response["message"] = e.args[0]
	return jsonify(response), status

# Token validator function. Helper method for creating a response
def tokenValidator(tokenString):
	response = {"message" : None}
	print("Token string passed in the request: ", tokenString)
	if Credential.isTokenValid( tokenString):
		print("Token is valid!")
		pass
	else:
		print("Token is invalid/missing?")
		status = httpstatus.UNAUTHORIZED
		response["message"] = "Invalid token or token has expired or "\
		+ "token parameter is missing in the request. "\
		+ "Please provide a valid token or get a new token invoking GET "\
		+ url_for("authenticate")
		return response, status
	return None

if __name__ == "__main__":
	app.debug = True
	app.run(host="0.0.0.0", port=5000, threaded=True)
