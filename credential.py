#!/usr/bin/env python

##############################################################################
#
# Authentication helper class
#
# @author: Satish Dash
#
###############################################################################

import base64
import datetime
import uuid

from db.dbconnect import MongoDB
from exceptions.exception import DBException

class Credential(object):
	''' Credential model helper class.'''

	def __init__(self, b64encodedString):
		self.credentials = b64encodedString
		self.username = None
		self.password = None
		self.token = None
		self.expiryTimeInUTC = None

	def _updateToken(self, tokencollname):
		newtoken = str(uuid.uuid4()).replace("-", "")
		expiryTime= datetime.datetime.utcnow() + datetime.timedelta(days=1)
		self.token = newtoken
		self.expiryTimeInUTC = expiryTime
		return tokencollname.update_one({"user":self.username}, {"$set":{"token":self.token, "expiry-time":expiryTime}}\
			, upsert=True)

	def getToken(self):
		tokencollname = None
		self.token = None
		if self.username:
			# Check if the existing token in token collection is still valid
			# Else create a new token in the database
			print("Ongoing transaction for user:", self.username)
			try:
				mongodb  = MongoDB()
				tokencollname = mongodb.getTokenCollection()
			except Exception as e:
				print(e.args)
				raise DBException("ERROR: Connecting to the database.")
			# Get the doc from credentials collection to validate.
			doc = tokencollname.find_one({"user":self.username})
			print("document:", doc)
			if doc:
				saved = doc.get("expiry-time")
				if saved and datetime.datetime.utcnow() <= saved:
					self.token = doc.get("token")
					print("Token has not expired:", self.token)
					self.expiryTimeInUTC = saved
				else:
					self._updateToken(tokencollname)
					print("New token is generated:", self.token)
			else:
				print("No document in:{} collection. Creating a new one.".format(tokencollname))
				self._updateToken(tokencollname)
				print("New token is generated:", self.token)
		return self.token

	@staticmethod
	def isTokenValid(tokenString):
		tokencollname = None
		try:
			mongodb  = MongoDB()
			tokencollname = mongodb.getTokenCollection()
		except Exception as e:
			print(e.args)
			raise DBException("ERROR: Connecting to the database.")
		# Validate the token
		if tokenString and tokenString.strip():
			doc = tokencollname.find_one({"token": tokenString})
			print("document:", doc)
			if doc:
				dbtoken = doc.get("token")
				if dbtoken and dbtoken.strip() and dbtoken.strip() == tokenString.strip():
					# Check if token has expired.
					curr = datetime.datetime.utcnow()
					saved = doc.get("expiry-time")
					if curr <= saved:
						print("Token is valid, has not expired.")
						return True
		return False

	def isValid(self):
		credcollname = None
		print("Hashed credentials:", self.credentials, type(self.credentials))
		try:
			mongodb  = MongoDB()
			credcollname = mongodb.getCredCollection()
		except Exception as e:
			print(e.args)
			raise DBException("ERROR: Connecting to the database.")
		try:
			# Get the encoded part from the credential string
			actual = self.credentials.split()
			credential = None
			if len(actual) > 1:
				credential = actual[1]
			elif len(actual) == 1:
				credential = actual[0]
			else:
				return False
			# Decode base64 encoded string
			string = base64.b64decode(credential.encode("utf-8")).decode("utf-8")

			# Separate out the username and password
			values = string.split(":")
			if len(values) == 2:
				self.username = values[0].strip()
				self.password = values[1].strip()
			else:
				return False
		except Exception as e:
			print(e.args)
			return False
		doc = credcollname.find_one({"user" : self.username})
		print("document:", doc.get("user"))
		if doc:
			# Validate password
			if self.password and doc.get("password") == self.password:
				print("Passwords match!")
				return True
		return False

	def getUserName(self):
		return self.username

	def getExpiryTime(self):
		return self.expiryTimeInUTC

	def __str__(self):
		return {"user":self.username,"token":self.token}

	def __repr__(self):
		return {"user":self.username,"token":self.token}
