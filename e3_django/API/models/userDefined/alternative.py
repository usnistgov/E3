from django.db import models
import logging

logger = logging.getLogger(__name__)


class Alternative(models.Model):
	"""
	Purpose: Initializes an Alternative object, verifies data fields.
	"""
	altID 		 = models.IntegerField(null=False)
	altName 	 = models.CharField(null=True, max_length=30)
	altBCNList 	 = models.JSONField(null=False, default=list)
	baselineBool = models.BooleanField()

	
	def __init__(self, *args, **kwargs):
		"""
		Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
		in addition to the above checking methods provided by models. Class variables are provided in the following table. 
		The STS document contains more information
		"""
		print("Alternative CONSTRUCTOR method called")
		# Add anything that should run BEFORE model validation.
		return super().__init__(*args, **kwargs)


	def validateAlternativeObject(self, objectList):
		"""
		Purpose: Verifies that all inputs are correct required data types and in valid range.
		Note: Does NOT actually create or return the Alternative object.
		Return: null
		"""
		obj = objectList.alternativeObject
		try:
			Alternative.objects.create(altID=obj.altID, altName=obj.altName, altBCNList=obj.altBCNList, baselineBool=obj.baselineBool)

			if not all(isinstance(x, int) for x in obj.altBCNList):
				logger.error("Err: %s", "all elements in altBCNList field must be of integer type.")
		except:
			logger.error("Err: %s", "Invalid input for Alternative object. Check that they are correct data types and in range.")
		
		# Check that list of bcnIDs exist, and all bcnIDs reference existing BCN objects.
		i = 0
		for x in objectList.bcnObject:			
			if x.bcnID != self.altBCNList[i]:
				logger.error("Err: %s", "alternativeBCNList does not match the list of bcnIDs of the object.")
			i+=1
    	
		# Check that only one alternative has baselineBool = True.
		boolCount = 0
		for x in objectList.bcnObject:
			if x.baselineBool:
				boolCount += 1
		if boolCount > 1:
			logger.error("Err: %s", "only one alternative can have baselineBool = True.")
		
		print("All inputs checked and verified. If no Err messages, Alternative object can be created.")

		return 