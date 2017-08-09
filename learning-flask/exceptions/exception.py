#!/usr/bin/env python

##########################################################################
#
# A exception module for respective model classes
#
# @author : Satish Dash
#
#########################################################################

class CandidateException(Exception):

	def __init__(self, message):
		super(CandidateException, self).__init__(message)
		self.message = message
		print(self.__class__.__name__ , self.message)


class ExperienceException(Exception):
	
	def __init__(self, message):
		super(ExperienceException, self).__init__(message)
		self.message = message
		print(self.__class__.__name__ , self.message)


class ProjectException(Exception):
		
	def __init__(self, message):
		super(ProjectException, self).__init__(message)
		self.message = message
		print(self.__class__.__name__ , self.message)


class DBException(Exception):
	def __init__(self, message):
		super(DBException, self).__init__(message)
		self.message = message
		print(self.__class__.__name__ , self.message)


class AuthenticationException(Exception):
	def __init__(self, message):
		super(AuthenticationException, self).__init__(message)
		self.message = message
		print(self.__class__.__name__ , self.message)