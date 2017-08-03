#!/usr/bin/env python

##########################################################################
#
# An ORM layer defining associations to DB relation - Project
#
# @author : Satish Dash
#
#########################################################################

from flask.ext.sqlalchemy import SQLAlchemy

# db object model
db = SQLAlchemy()

class Project(db.Model):

	__tablename__ = "project"

	id = db.Column(db.Integer, primary_key=True)
	uuid = db.Column(db.String(32), nullable=False)
	name = db.Column(db.String(100), nullable=False, unique =True)
	description = db.Column(db.String(300), nullable = True)
	start_date = db.Column(db.DateTime(), nullable=False)
	end_date = db.Column(d.DateTime(), nullable =True)

	def __init__(uuid, name, description, start_date, end_date):
		self.uuid = uuid
		self.name = name
		self.description = description
		self.start_date = start_date
		self.end_date = end_date

	@property
	def uuid(self):
		return self.uuid
	
	@uuid.setter
	def uuid(self, uuid):
		self.uuid = uuid

	@property
	def name(self):
		return self.name
	
	@name.setter
	def name(self, name):
		self.name = name

	@property
	def description(self):
		return self.description
	
	@description.setter
	def description(self,desc):
		self.description = desc

	@property
	def start_date(self):
		return self.start_date
	
	@start_date.setter
	def start_date(self, start_date):
		self.start_date = start_date

	@property
	def end_date(self):
		return self.end_date
	
	@end_date.setter
	def end_date(self, end_date):
		self.end_date = end_date

	@property
	def serialize(self):
		return {
			'projectID':self.uuid,
			'name': self.name,
			'description': se;f.description,
			'start_date' : self.start_date,
			'end_date': se;f.end_date
		}
	
	def 
