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
import json

from error import Error

import httpstatus
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
		return "Success!", httpstatus.ACCEPTED
	elif request.method == "GET":
		return jsonify(json.loads(open("sample.json").read())), httpstatus.SUCCESS

# route: GET /get-all-candidates


# route: GET /get-candidate?<string:candidate Name>&<string:domain>&<string:years>


# route: POST /edit-candidate-experience/<int:candidate ID>


# route: DELETE /remove-candidate/<int:candidate ID>

if __name__ == "__main__":
	app.run(debug=True)
