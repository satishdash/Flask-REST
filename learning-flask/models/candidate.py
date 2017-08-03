#!/usr/bin/env python

##########################################################################
#
# A model class defining - Candidate
#
# @author : Satish Dash
#
#########################################################################

import json

from experience import Experience
from exceptions.exception import CandidateException, ExperienceException, ProjectException

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
			if fname in self.candidateDict and self.candidateDict.get(fname):
				print(fname, "is present in the profile.")
			else:
				raise CandidateException("'" + fname + "'" + " key is missing from the profile. Please do provide a " + fname )
				
			if "last_name" in self.candidateDict:
				print(lname, "is present in the profile.")
			else:
				raise CandidateException("'" + lname + "'" + " key is missing from the profile. Please do provide a " + lname )
		return True
	
	def _validateCandidateExp(self):
		# check if experience is present
		expe = "experience"
		if self.candidateDict.get(expe):
			Experience exp = Experience(json.dumps(self.candidateDict.get(expe)))
			return exp.isExperienceValid()
		else:
			raise CandidateException("'" + expe + "'" + " list is missing from Candidate profile. Please add an experience list.")



	def isProfileValid(self):
		return self._validateCandidateName() and self._validateCandidateExp()
		



