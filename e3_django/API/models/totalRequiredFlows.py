from django.db import models
import logging

logger = logging.getLogger(__name__)

class TotalRequiredFlows(models.Model):
	"""
	Purpose: Initializes a TotalRequiredFlows object, verifies data fields.
	"""
	#altID = models.IntegerField(default=None)
	baselineBool = models.BooleanField()
	sensBool = models.BooleanField(default=False)
	uncBool = models.BooleanField(default=False)

	# Below is varList, consisting of 20 variables
	totCostNonDisc  = models.JSONField(default=list)
	totCostDisc  = models.JSONField(default=list)
	totCostNonDiscInv  = models.JSONField(default=list)
	totCostDiscInv  = models.JSONField(default=list)
	totCostNonDiscNonInv  = models.JSONField(default=list)
	totCostDiscNonInv  = models.JSONField(default=list)
	totBenefitsNonDisc  = models.JSONField(default=list)
	totBenefitsDisc  = models.JSONField(default=list)
	totCostDir  = models.JSONField(default=list)
	totCostInd  = models.JSONField(default=list)
	totCostExt  = models.JSONField(default=list)
	totCostDirDisc  = models.JSONField(default=list)
	totCostIndDisc  = models.JSONField(default=list)
	totCostExtDisc  = models.JSONField(default=list)
	totBenefitsDir  = models.JSONField(default=list)
	totBenefitsInd  = models.JSONField(default=list)
	totBenefitsExt  = models.JSONField(default=list)
	totBenefitsDirDisc  = models.JSONField(default=list)
	totBenefitsIndDisc  = models.JSONField(default=list)
	totBenefitsExtDisc  = models.JSONField(default=list)
	

	def __init__(self, *args, **kwargs): 
		"""
		Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
		in addition to the above checking methods provided by models. Class variables are provided in the following table. 
		The STS document contains more information
		"""
		print("TotalRequiredFlows CONSTRUCTOR method called")
		# Add anything that should run BEFORE model validation.
		return super().__init__(*args, **kwargs)


	def validateTotalRequiredFlows(self, totalReqFlowsObject):
		"""
		Purpose: Further verifies that all lists contain floats.
		Return: null
		"""
		obj = totalReqFlowsObject
		try:
			TotalRequiredFlows.objects.create( #altID=obj.altID, 
				baselineBool=obj.baselineBool, sensBool=obj.sensBool, uncBool=obj.uncBool, \
				totalCostNonDisc=obj.totalCostNonDisc, totCostDisc=obj.totCostDisc, totCostNonDiscInv=obj.totCostNonDiscInv, totCostDiscInv=obj.totCostDiscInv, \
				totCostNonDiscNonInv=obj.totCostNonDiscNonInv, totCostDiscNonInv=obj.totCostDiscNonInv, totBenefitsNonDisc=obj.totBenefitsNonDisc, \
				totBenefitsDisc=obj.totBenefitsDisc, totCostDir=obj.totCostDir, totCostInd=obj.totCostInd, totCostExt=obj.totCostExt, totCostDirDisc=obj.totCostDirDisc, \
				totCostIndDisc=obj.totCostIndDisc, totCostExtDisc=obj.totCostExtDisc, totBenefitsDir=obj.totBenefitsDir, totBenefitsInd=obj.totBenefitsInd, \
				totBenefitsExt=obj.totBenefitsExt, totBenefitsDirDisc=obj.totBenefitsDirDisc, totBenefitsIndDisc=obj.totBenefitsIndDisc, totBenefitsExtDisc=obj.totBenefitsExtDisc)

			for var in [obj.totCostNonDisc, obj.totCostDisc, obj.totCostNonDiscInv, obj.totCostDiscInv, obj.totCostNonDiscNonInv, obj.totCostDiscNonInv, \
				obj.totBenefitsNonDisc, obj.totBenefitsDisc, obj.totCostDir, obj.totCostInd, obj.totCostExt, obj.totCostDirDisc, obj.totCostIndDisc, obj.totCostExtDisc, \
					obj.totBenefitsDir, obj.totBenefitsInd, obj.totBenefitsExt, obj.totBenefitsDirDisc, obj.totBenefitsIndDisc, obj.totBenefitsExtDiszc]:
				if not all(isinstance(x, float) for x in var):
					logger.error("Err: all elements in %s field must be of float type.", var)

		except:
			logger.error("Err: %s", "Invalid input to create TotalRequiredFlows object. Check that they are correct data type and in range.")


	def addFlow(self, flowName, flow):
		"""
		Purpose: Based on provided flowName, adds the flow to the appropriate variable. 
		Note: flowName must be a string with the same name as the variable, without the enclosing brackets.
		"""
		var = self.flowName
		var.append(flow)		
		logger.info("Info: flow %s successfully added to flow %s", flow, flowName)
		return


	def updateFlow(self, flowName, flow):
		"""
		Purpose: Based on provided flowName, resets current flow to the input flow.
		Note: flowName must be a string with the same name as the variable, without the enclosing brackets.
		"""
		self.flowName = flow
		logger.info("Info: flow %s successfully updated to %s", flowName, flow)
		return


	def updateAllFlows(self, flowsList): 
		"""
		Purpose: Updates all flows in the flowList simultaneously.

		Note: Input order is the same as order that variables appear in the object.
		flowsList is a list of lists, outer list is length of however many list variables there are in the class (20) 
		(list of 20 lists 'totsCostNonDisc->totBenefitsExtDisc', internal lists will be of length studyLength + 1)
		"""
		self.totCostNonDisc = flowsList[0]
		self.totCostDisc  = flowsList[1]
		self.totCostNonDiscInv  = flowsList[2]
		self.totCostDiscInv  = flowsList[3]
		self.totCostNonDiscNonInv  = flowsList[4]
		self.totCostDiscNonInv  = flowsList[5]
		self.totBenefitsNonDisc  = flowsList[6]
		self.totBenefitsDisc  = flowsList[7]
		self.totCostDir  = flowsList[8]
		self.totCostInd  = flowsList[9]
		self.totCostExt  = flowsList[10]
		self.totCostDirDisc  = flowsList[11]
		self.totCostIndDisc  = flowsList[12]
		self.totCostExtDisc  = flowsList[13]
		self.totBenefitsDir  = flowsList[14]
		self.totBenefitsInd  = flowsList[15]
		self.totBenefitsExt  = flowsList[16]
		self.totBenefitsDirDisc  = flowsList[17]
		self.totBenefitsIndDisc  = flowsList[18]
		self.totBenefitsExtDisc  = flowsList[19]

		logger.info("Info: All flows in flowList were successfully updated.")
		return