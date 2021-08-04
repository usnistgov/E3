from django.db import models

class Sensitivity(models.Model):

	globalVarBool = models.BooleanField(null= True)
	altID 		  = models.IntegerField(null=True, unique=True)
	bcnID 		  = models.CharField(null=True, max_length=30, default='')
	varName  	  = models.CharField(null=True, max_length=30, default='')
	diffType 	  = models.CharField(null=True, max_length=30, default='')
	diffVal 	  = models.DecimalField(null=True, max_digits=7, decimal_places=2)


	"""
	Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
        in addition to the above checking methods provided by models. Class variables are provided in the following table. 
        The STS document contains more information
	@classmethod
    def __init__(self):
        if self.globalVarBool == True:
            if not self.altID:
                raise Exception("AltID cannot be null when globalVarBool is True")
            if not self.bcnID:
                raise Exception("BCNID cannot be null when globalVarBool is True")
        return

    
    def validateSensitivityObject(objectList):
        if not all(objectList):
            raise Exception("At least one value in objectList is missing")

        if not objectList.bcnId: # bcnID references an existing BCN object
            raise Exception("BCN ID does not reference an existing BCN object")

        # check initialOcc doesn't occur after recurEndDate, other valid ranges for  variable being carried over
        return
	"""