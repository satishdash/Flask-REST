#!/usr/bin/env python

##########################################################################
#
# A model class defining - Candidate
#
# @author : Satish Dash
#
#########################################################################

import json

from models.experience import Experience
from exceptions.exception import CandidateException

class Candidate(object):


	def __init__(self, candidateProfileJson):
		self.candidateJson = candidateProfileJson
		self.candidateDict = None

	def _validateCandidateName(self):
		if not self.candidateDict:
			try:
				self.candidateDict = json.loads(self.candidateJson)
			except:
				raise CandidateException("Candidature json is invalid. JSON is incorrect. \
				Please post a correctly formatted JSON.")
			fname = "first_name"
			lname = "last_name"
			if self.candidateDict.get(fname):
				print(fname, "is present in the profile.")
			else:
				raise CandidateException("'" + fname + "'" + " key or value is missing from the profile. \
				Please do provide a " + fname )
				
			if self.candidateDict.get(lname):
				print(lname, "is present in the profile.")
			else:
				raise CandidateException("'" + lname + "'" + " key or value is missing from the profile. \
				Please do provide a " + lname )
		return True
	
	def _validateCandidateExp(self):
		# check if experience is present
		expe = "experience"
		if self.candidateDict.get(expe):
			exp = Experience(json.dumps(self.candidateDict.get(expe)))
			return exp.isExperienceValid()
		else:
			raise CandidateException("'" + expe + "'" + " list is missing from the Candidate profile. \
			Please add an experience list.")



	def isProfileValid(self):
		return self._validateCandidateName() and self._validateCandidateExp()
		

