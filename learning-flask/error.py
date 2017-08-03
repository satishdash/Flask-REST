#!/usr/bin/env python

##############################################################################
#
# Error model response class for the application
#
# @author: Satish Dash
#
###############################################################################

import json

class Error(object):
	''' Error model response class.'''
	
	def __init__(self, msg, status):
		self.message = msg
		self.code = status
	
	# serialize data
	def serialize(self):
		return {
			'code': self.code,
			'message'  :self.message
		}

	def __str__(self):
		return json.dumps(self.serialize())

	def __repr__(self):
		return json.dumps(self.serialize())
