#!/usr/bin/env python

##########################################################################
#
# A model class for validating - Experience
#
# @author : Satish Dash
#
#########################################################################

import json

from models.project import Projects
from exceptions.exception import ExperienceException
from models import properties

class Experience(object):
	
	def __init__(self, experienceJson):
		self.experienceJson = experienceJson
		self.experienceList = None
	

	def _validateCandidateExp(self):
		if self.experienceJson:
			try:
				self.experienceList = json.loads(self.experienceJson)
			except:
				raise ExperienceException("Experience is in incorrect JSON format."
				+ " Please provide experience in a proper format. {}".format(properties.SAMPLE_API_REF))

			if isinstance(self.experienceList, list) and len(self.experienceList) > 0:
				domain = "domain"
				years = "years"
				proj = "projects"
				
				# loop through all the experience list to validate domain and years of experience
				for exp in self.experienceList:
					if domain in exp and exp.get(domain):
						print(domain + " key is present -> {}".format(exp.get(domain)))
					else:
						raise ExperienceException(domain + " key is missing in one of the " 
						+ "experiences of this profile or has no value. {}".format(exp))
					if years in exp and exp.get(years):
						try:
							print( years + " of domain expertise is : {}".format(float(exp[years])))
						except:
							raise ExperienceException(years + "{} format is incorrect. Must be a number.".format(exp[years]))
					else:
						raise ExperienceException(years + " key is missing or value is invalid (must be > 0).")
					
					# validate projects in this domain
					if exp.get(proj):
						prj = Projects(json.dumps(exp[proj]))
						if prj.isProjectValid():
							continue
						else:
							pass
					else:
						raise ExperienceException("'" + proj + "' key is missing in this experience. "
						+ "Please add a valid list of projects. {}".format(properties.SAMPLE_API_REF))
			else:
				raise ExperienceException("Experience list is invalid or empty. Please provide a valid experience list.")
		else:
			raise ExperienceException("Candidate's experience is missing from the profile. Please add a valid experience list.")
		return True

	
	def isExperienceValid(self):
		return self._validateCandidateExp()

