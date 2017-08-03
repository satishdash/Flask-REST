#!/bin/bash

##################################################################################################
# 
# A flask application server with defined web routes.
# [ REST based recruiter data store system]
#
# @author : Satish Dash
#
##################################################################################################

from flask import Flask, jsonify, request

from error import Error

import httpstatus

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
		pass 
	err = Error("The request type is incorrect. Only POST requests are allowed.", httpstatus.BAD_REQUEST)
	return jsonify(err.serialize()), httpstatus.BAD_REQUEST


# route: GET /get-all-candidates


# route: GET /get-candidate/<string:candidateName>


# route: POST /edit-candidate-experience/<int:candidateId>


# route: DELETE /remove-candidate/<string:candidateName>

if __name__ == "__main__":
	app.run(debug=True)
