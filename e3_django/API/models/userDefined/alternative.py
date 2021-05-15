from django.db import models

class Alternative(models.Model):
	"""
	Purpose: Initializes an Alternative object 
	"""
	# Verify data type and length as Alternative object is created.
	altID 		 = models.IntegerField(null=False)
	altName 	 = models.CharField(max_length=30, null=False)
	altBCNList 	 = models.JSONField(null=True, default=list)
	baselineBool = models.BooleanField()

	"""
	Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
    in addition to the above checking methods provided by models. Class variables are provided in the following table. 
    The STS document contains more information
	@classmethod
    def __init__(self, *args, **kwargs):
        if not all(isinstance(x, int) for x in self.alternativeBCNList):
            raise Exception("Incorrect data type: alternativeBCNList must be a list of unique integers")
        # TODO:  Check that self.alternativeBCNList is a list of bcnIDs associated with the alternativeID (required)
        return 
	"""

	def validateAlternativeObject(self, objectList):
		boolCount = 0
		for bcnObject in objectList.bcnObject:
			for x in bcnObject:
				# check all bcnID reference existing BCN objects.
				if not x.bcnID:
					raise Exception("BcnID does not exist for one or more BCN Objects")
				if x.baselineBoolCount == True:
					boolCount += 1
				if boolCount >= 1:
					raise Exception("Only one alternative can have baselineBool = True")
		return 