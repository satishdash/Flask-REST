#!/usr/bin/env python

##########################################################################
#
# An ORM layer defining associations to DB relation - Candidate
#
# @author : Satish Dash
#
#########################################################################

from flask.ext.sqlalchemy import SQLAlchemy

# db object model
db = SQLAlchemy()

class Candidate(db.Model):

	__tablename__ = "candidate"

	id = db.Column(db.Integer, primary_key=True)
	first_name = db.Column(db.String(100), nullable=False)
	last_name = db.Column(db.String(100), nullable=False)
	experience = db.relationship('experience', backref='candidate', lazy=True)

	def __init__(first_name, last_name):
		self.first_name = first_name
		self.last_name= last_name

	@property
	def first_name(self):
		return self.first_name
	
	@first_name.setter
	def first_name(self, first_name):
		self.first_name = first_name

	@property
	def last_name(self):
		return self.last_name
	
	@last_name.setter
	def last_name(self, last_name):
		self.last_name = last_name

	@property
	def serialize(self):
		return {
			'candidateID' : self.id,
			'first_name' : self.first_name,
			'last_name' : self.last_name,
			'experience' : self.experience
		}
	
