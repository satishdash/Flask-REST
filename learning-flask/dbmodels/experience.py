#!/usr/bin/env python

##########################################################################
#
# An ORM layer defining associations to DB relation - Experience
#
# @author : Satish Dash
#
#########################################################################

from flask.ext.sqlalchemy import SQLAlchemy

# db object model
db = SQLAlchemy()

class Experience(db.Model):

	__tablename__ = "experience"

	id = db.Column(db.Integer, primary_key=True)
	domain = db.Column(db.String(100), nullable=False, unique =True)
	years = db.Column(db.Integer, nullable = False)
	projects = db.Column('project', backref='experience', lazy=True)

	def __init__(domain, years):
		self.domain = domain
		self.years = years

	@property
	def domain(self):
		return self.domain
	
	@domain.setter
	def domain(self, domain):
		self.domain = domain

	@property
	def years(self):
		return self.years
	
	@name.setter
	def years(self, years):
		self.years = years

	@property
	def serialize(self):
		return {
			'ExperienceID' : self.id,
			'domain' : self.domain,
			'years_of_experience' : self.years,
			'projects': self.projects
		}
	
