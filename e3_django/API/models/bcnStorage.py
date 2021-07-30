from django.db import models
import logging

logger = logging.getLogger(__name__)


class BCNStorage(models.Model):
	"""
	Purpose: Initializes a BCN Storage object, verifies data fields.
	"""
	bcnID 			= models.IntegerField(null=False)
	bcnName 		= models.CharField(null=True, max_length=30, default="")
	altID 			= models.JSONField(default=list, unique=True)
	bcnType 		= models.CharField(null=True, max_length=30) 
	bcnSubType 		= models.CharField(null=True, max_length=30) 
	tag 			= models.CharField(max_length=30, default="") 
	bcnNonDiscFlow 	= models.JSONField(default=list)
	bcnDiscFlow 	= models.JSONField(default=list)
	quantList 		= models.JSONField(default=list)
	quantUnits 		= models.CharField(max_length=30, null=False, default="")
	sensBool  		= models.BooleanField(null=True)
	sensFlowNonDisc = models.JSONField(default=list)
	sensFlowDisc	= models.JSONField(default=list)
	sensQuantList 	= models.JSONField(default=list)
	uncBool 		= models.BooleanField(null=True)
	uncFlowNonDisc 	= models.JSONField(default=list)
	uncFlowDisc		= models.JSONField(default=list)
	uncQuantList 	= models.JSONField(default=list)
	

	def __init__(self, *args, **kwargs):
		"""
		Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
    	in addition to the above checking methods provided by models. Class variables are provided in the following table. 
    	The STS document contains more information
		"""
		print("BCN Storage CONSTRUCTOR method called")
		# Add anything that should run BEFORE model construction.
		return super().__init__(*args, **kwargs)


	def validateBCNStorageObject(self, bcnStorageObject):
		obj = bcnStorageObject
		try:
			BCNStorage.objects.create(bcnID=obj.bcnID, bcnName=obj.bcnName, altID=obj.altID, bcnType=obj.bcnType, bcnSubType=obj.bcnSubType, \
				tag=obj.tag, bcnNonDiscFlow=obj.bcnNonDiscFlow, bcnDiscFlow=obj.bcnDiscFlow, quantList=obj.quantList, quantUnits=obj.quantUnits, \
				sensBool=obj.sensBool, sensFlowNonDisc=obj.sensFlowNonDisc, sensFlowDisc=obj.sensFlowDisc, sensQuantList=obj.sensQuantList, \
				uncBool=obj.uncBool, uncFlowNonDisc=obj.unFlowNonDisc, uncFlowDisc=obj.uncFlowDisc, uncQuantList=obj.uncQuantList)

			# Check data type in list fields
			if not all(isinstance(x, int) for x in self.altID):
				logger.error("Err: %s", "all elements in altID field must be of integer type.")
        
			if not all(isinstance(x, float) for x in self.bcnNonDiscFlow):
				logger.error("Err: %s", "all elements in bcnNonDiscFlow field must be of float type.")
			
			if not all(isinstance(x, float) for x in self.bcnDiscFlow):
				logger.error("Err: %s", "all elements in bcnDiscFlow field must be of float type.")
			
			if not all(isinstance(x, float) for x in self.quantList):
				logger.error("Err: %s", "all elements in quantList field must be of float type.")

			if not all(isinstance(x, int) for x in self.sensFlowNonDisc):
				logger.error("Err: %s", "all elements in sensFlowNonDisc field must be of integer type.")
			
			if not all(isinstance(x, float) for x in self.sensFlowDisc):
				logger.error("Err: %s", "all elements in sensFlowDisc field must be of float type.")

			if not all(isinstance(x, float) for x in self.sensQuantList):
				logger.error("Err: %s", "all elements in sensQuantList field must be of float type.")
			
			if not all(isinstance(x, float) for x in self.uncFlowNonDisc):
				logger.error("Err: %s", "all elements in uncFlowNonDisc field must be of float type.")

			if not all(isinstance(x, float) for x in self.uncFlowDisc):
				logger.error("Err: %s", "all elements in uncFlowDisc field must be of float type.")

			if not all(isinstance(x, float) for x in self.uncQuantList):
				logger.error("Err: %s", "all elements in uncQuantList field must be of float type.")

			# TODO: Check bcnType is equivalent to bcn.type for bcnID
			# TODO: Check subType is equivalent to bcn.subType for bcnID
			# TODO: Check tag is equivalent to bcn.tag for bcnID

		except:
			logger.error("Err: %s", "Invalid input for BCNStorage object. Check that they are correct data type and in range.")


	def updateSensFlows(self, newSensFlowNonDisc, newSensFlowDisc, newSensFlowQuant):
		"""
		Purpose: Updates the sensitivity flows with the input flows.
		"""
		self.sensFlowNonDisc = newSensFlowNonDisc
		self.sensFlowDisc = newSensFlowDisc
		self.sensQuantList = newSensFlowQuant

		logger.info("Note: %s", "Sensitivity flows successfully updated with new values.")
		return


	def updateUncFlows(self, newUncFlowNonDisc, newUncFlowDisc, newUncFlowQuant):
		"""
		Purpose: Updates the uncertainty flows with input flows.
		"""
		self.uncFlowNonDisc = newUncFlowNonDisc
		self.uncFlowDisc = newUncFlowDisc
		self.uncQuantList = newUncFlowQuant

		logger.info("Note: %s", "Sensitivity flows successfully updated with new values.")
		return
