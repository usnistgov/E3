from django.db import models
import logging

logger = logging.getLogger(__name__)

class TotalOptionalFlows(models.Model):
	"""
	Purpose: Initializes a TotalOptionalFlows object, verifies data fields.
	"""
	altID = models.IntegerField(null=False, default=None)
	sensBool = models.BooleanField(default=False)
	uncBool = models.BooleanField(default=False)
	bcnType  = models.CharField(null=False, max_length=30, default="")
	bcnSubType = models.CharField(null=True, max_length=30)
	bcnTag = models.JSONField(null=True, default=list) 
	totalTagFlowDisc = models.JSONField(default=list)
	totTagQ = models.JSONField(default=list)
	quantUnits = models.CharField(max_length=30, default="dollars")

		
	def validateTotalOptionalFlows(self, totalOpFlowsObject):
		"""
        Purpose: Verifies that all inputs are correct required data types and in valid range. 
		Note: Does NOT actually create or return the TotalOptionalFlows object.
		Return: null
        """
		obj = totalOpFlowsObject
		try: 
			TotalOptionalFlows.object.create(altID=obj.altID, sensBool=obj.sensBool, uncBool=obj.uncBool, bcnType=obj.bcnType, \
				bcnSubType=obj.bcnSubType, bcnTag=obj.bcnTag, totalTagFlowDisc=obj.totalTagFlowDisc, totTagQ=obj.totTagQ, \
				quantUnits=obj.quantUnits)

			if not all(isinstance(x, str) for x in self.bcnTag):
				logger.error("Err: %s", "all elements in bcnTag field must be of string type.")
			
			if not all(isinstance(x, float) for x in self.totTagFlowDisc):
				logger.error("Err: %s", "all elements in totTagFlowDisc field must be of float type.")
		
			if not all(isinstance(x, float) for x in self.totTagQ):
				logger.error("Err: %s", "all elements in totTagQ field must be of float type.")

		except:
			logger.error("Err: %s", "Invalid input to create TotalOptionalFlows object.  Check that they are correct data type and in range.")

		return
	
	
	def addFlow(self, cashFlowBool, flow):
		"""
		Purpose: Based on cashFlowBool, add input flow to current flow values.
		"""
		if cashFlowBool: # if cashFlowBool is True
			self.totTagFlowDisc += flow
			logger.info("Info: flow %s successfully added to totTagFlowDisc.", flow)

		else: # if cashFlowBool is False
			self.totTagQ += flow
			logger.info("Info: flow %s successfully added to totTagQ.", flow)

		return

	
	def updateFlow(self, cashFlowBool, flow):
		"""
		Purpose: Based on cashFlowBool, reset current flow to the input flow value.
		"""
		if cashFlowBool: # if cashFlowBool is True
			self.totTagFlowDisc = flow
			logger.info("Info: flow %s successfully reset to totTagFlowDisc.", flow)
 
		else: # if cashFlowBool is False
			self.totTagQ = flow
			logger.info("Info: flow %s successfully reset to totTagQ.", flow)

		return