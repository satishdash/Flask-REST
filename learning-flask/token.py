#!/usr/bin/env python

##############################################################################
#
# Token model class
#
# @author: Satish Dash
#
###############################################################################

from db.dbconnect import MongoDB
from exceptions.exception import AuthenticationException

class Token(object):
	''' Token model definition class.'''

	def __init__(self, **kwargs):
		if not kwargs:
			raise AuthenticationException("Credential parameters for API authentication not found."\
				+ "Please pass valid credentials/a token.")
		self.username = kwargs.get("username")
		self.password= kwargs.get("password")
		self.token = kwargs.get("token")

	def getToken(self):
		pass

	def isTokenValid(self):
		pass

	def __str__(self):
		return self.__class__.__name__ + "(user={},token={})".format(self.username, self.token)

	def __repr__(self):
		return self.__str__()
