from django.db import models

class Alternative(models.Model):
	"""
	Purpose: Initializes an Alternative object 
	"""
	altID 		 = models.IntegerField(null=False)
	altName 	 = models.CharField(max_length=30, null=False)
	altBCNList 	 = models.JSONField(null=True, default=list)
	baselineBool = models.BooleanField()


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