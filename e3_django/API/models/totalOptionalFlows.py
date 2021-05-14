from django.db import models

class TotalOptionalFlows(models.Model):
	"""
	Purpose: Initializes an AlternativeSummary object
	"""
	# Verify data types and length as Object is created
	altID = models.IntegerField()
	sensBool = models.BooleanField()
	uncBool = models.BooleanField()
	#bcnType  = bcn.type variable stored here for convenience - see __init__
	#bcnSubType = bcn.type variable stored here for convenience - see __init__
	#bcnTag = bcn.tag, user defined tag to set up custom groups of bcn objects
	totalTagFlowDisc = models.JSONField()
	totTagQ = models.JSONField()
	quantUnits = models.CharField(max_length=30)


	def __init__(self):
		self.bcnType = bcn.bcnType
		self.bcnSubType = bcnSubType	

		if not all(isinstance(x, float) for x in self.totTagFlowDisc):
			raise Exception("Incorrect data type: totTagFlowDisc must be a list of floats")
		
		if not all(isinstance(x, float) for x in self.totTagQ):
			raise Exception("Incorrect data type: totTagQ must be a list of floats")
			return

		
	def addFlow(cashFlowBool, flow):
		"""
		Purpose: Based on cashFlowBool, add input flow to current flow values.
		"""
		if cashFlowBool == True:
			self.totTagFlowDisc += flow
		if cashFlowBool == False:
			self.totTagQ += flow
		return


	def updateFlow(cashFlowBool, flow):
		"""
		Purpose: Based on cashFlowBool, reset current flow to the input flow value.
		"""
		if cashFlowBool == True:
			self.totTagFlowDisc = flow
		elif cashFlowBool == False:
			self.totTagQ = flow
		return