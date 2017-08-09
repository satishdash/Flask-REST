#!/usr/bin/env python

##########################################################################
#
# A module for getting connection to a database (Singleton)
#
# @author : Satish Dash
#
#########################################################################

import os
from configparser import ConfigParser

from exceptions.exception import DBException
import pymongo as pm

class Borg(object):
	'''shared state initialized class.'''
	_shared_state = {}

	def __init__(self):
		super(Borg, self).__init__()
		self.__dict__ = Borg._shared_state
	
	def __str__(self):
		return str(Borg._shared_state)

class MongoDB(Borg):
	'''Mongo DB connection class.'''

	def __init__(self):
		super(MongoDB, self).__init__()
		if self._shared_state.get("mongodb"):
			pass
		else:
			self.config = ConfigParser()
			try:
				ini_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dbconfig.ini")
				self.cfg = self.config.read(ini_file)
				self.user = self.config.get("mongodb", "username")
				self.pwd = self.config.get("mongodb", "password")
				self.conn = self.config.get("mongodb", "connection")
				self.dbname = self.config.get("mongodb", "dbname")
				self.collname = self.config.get("mongodb", "collname")
				self.connection = self.conn.format(self.user, self.pwd, self.dbname)
			except Exception as e:
				print("exception: " + e.args[0]) 
				raise DBException(str(e.args) + " Persistent storage configuration could not be formulated."
				" Cannot proceed to get connection.")
			try:
				self.client = pm.MongoClient(self.connection, tz_aware=True)
				#  update the connection object in the state permanently
				self._shared_state.update({"mongodb":self.client})
			except Exception as e:
				print(e.args[0])
				raise DBException("Failed to setup/create a connection to MongoDB server.")


	def getConnection(self):
		if self._shared_state.get("mongodb"):
			return self._shared_state["mongodb"].get_database(self.dbname)
		raise DBException("Connection to persistent storage not available.")
	
	def getCollection(self):
		if self._shared_state.get("mongodb"):
			return self.getConnection().get_collection(self.collname)
		raise DBException("Connection to collection :{} in DB not available.".format(self.collname))


	def __str__(self):
		return str(self._shared_state)

	def __repr__(self):
		return str(self._shared_state)

class Example(MongoDB):
	def __init__(self):
		super(Example, self).__init__()
		self._shared_state.update({"example":self.__class__.__name__})

	def __str__(self):
		return str(self._shared_state)

