#!/usr/bin/env python

##########################################################################
#
# A model class for validating - Project
#
# @author : Satish Dash
#
#########################################################################


from datetime import datetime
import json

from exceptions.exception import ProjectException
from models import properties

class Projects(object):
	
	def __init__(self, projectJson):
		self.projectJson = projectJson
		self.projectList = None
	

	def _validateProjectList(self):
		if self.projectJson:
			try:
				self.projectList = json.loads(self.projectJson)
			except:
				raise ProjectException("Project list mentioned is in incorrect JSON format. "
				+ "Please provide a valid list of project in the experience section. {}".format(properties.SAMPLE_API_REF))

			name = "name"
			desc = "description"
			start_date = "start_date"
			end_date = "end_date"
			# ignore project name
			# loop through all the projects if present
			if isinstance(self.projectList, list) and len(self.projectList) > 0:
				for p in self.projectList:
					if p.get(desc):
						pass
					else:
						raise ProjectException(desc + " key is missing from this project "
						+ "or value is empty. Value={}".format(p))

					if p.get(start_date):
						try:
							sd = datetime.strptime(p.get(start_date), "%B-%Y")
						except Exception as e:
							raise ProjectException(start_date + " is not in the required format, "
							+ "Value={}. Required format=<Month-YYYY>".format(p.get(start_date)))

					else:
						raise ProjectException(start_date + " key is missing from this project "
						+ " or value is empty. {}".format(p.get(start_date)))

					if p.get(end_date):
						try:
							ed = datetime.strptime(p.get(end_date), "%B-%Y")
						except:
							raise ProjectException(end_date + " is not in the required format, "
							+ "Value={}. Required format=<Month-YYYY>".format(p.get(end_date)))

			else:
				raise ProjectException("List of projects is in incorrect format or is empty. {}".format(properties.SAMPLE_API_REF))

		else:
			raise ProjectException("List of projects is missing from the experience profile.")
		return True

	def isProjectValid(self):
		return self._validateProjectList()


