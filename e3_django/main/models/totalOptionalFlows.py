sys.path.insert(1, '/e3_django/main/libraries')
import cashFlow
from .userDefined import bcn

class TotalOptionalFlows(models.Model):
    """
    Purpose: Stores total cash flows for a single altID-tag combination.
    """
    # Verify data type and length as Object is created.
    altID = models.IntegerField()
    sensBool = models.BooleanField()
    uncBool = models.BooleanField()
    #bcnType = bcn.type variable stored here for convenience
    #bcnSubType = bcn.type variable stored here for convenience
    #bcnTag = – bcn.tag, user defined tag to set up custom groups of bcn objects
    totTagFlowDisc = models.JSONField()
    totTagQ = models.JSONField()
    quatnUnits = models.CharField()


	def __init__(self):

		self.bcnType = bcn.bcnType # bcn.bcnType variable stored here for convenience
		self.bcnSubType = bcn.bcnSubType # bcn.bcnSubType variable stored here for convenience
		
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



	def upadateFlow(cashFlowBool, flow):
		"""
		Purpose: Based on cashFlowBool, reset current flow to the input flow value.
		"""
		if cashFlowBool == True:
			self.totTagFlowDisc = flow

		elif cashFlowBool == False:
			self.totTagQ = flow

		return