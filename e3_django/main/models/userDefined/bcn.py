from django.db import models
from main.libraries import discounting, cashFlow, validateRead
from main.models import alternativeSummary, totalRequiredFlows, totalOptionalFlows, sensitivitySummary, uncertaintySummary
from django.core.validators import MaxValueValidator, MinValueValidator
import logging

class BCN(models.Model):
    """
    Purpose: Stores total flows for a single BCN.
    """
    # Verify data type and range as BCN object is created (In addition to var check in __init__)
    altID = models.IntegerField()
    bcnID = models.IntegerField(unique=True) # Whole digit must be unique to BCN
    bcnType  = models.CharField(max_length=30) # called 'type' in pseudocode; changed because 'type' is a reserved keyword.
    bynSubType = models.CharField(max_length=30)
    bcnName = models.CharField(max_length=30)
    bcnTag = models.JSONField() 
    initialOcc = models.IntegerField(validators=[MinValueValidator(0)]) # TODO: Check that this occurs at a valid timestep, check that value is less than studyPeriod.
    bcnRealBool = models.BooleanField()
    bcnInvestBool = models.BooleanField()
    bcnLife = models.IntegerField(validators=[MinValueValidator(1)])
    ryBool = models.BooleanField()
    recurBool = models.BooleanField()
    recurInterval = models.IntegerField(validators=[MinValueValidator(1)])
    recurVarRate = models.CharField(max_length=30)
	# recurVarValue = models.JSONField() # Included in third table (of Pseudocode 5. BCN Class), but not in first table; Omitted for now
    recurEndDate = models.DateTimeField(auto_now_add=True, validators=[MinValueValidator(initialOcc)]) # TODO: check that value is less than studyPeriod.
    valuePerQ = models.DecimalField(max_digits=7, decimal_places=2)
    quant = models.DecimalField(max_digits=7, decimal_places=2)
    quantVarRate = models.CharField(max_length=30)
    quantVarValue = models.JSONField()
    quantUnit = models.CharField(max_length=30) # If blank, report blank? See (*) line 
	# further check in __init__ constructor. See below


    @classmethod
    def __init__(self):
        """
        Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
        in addition to the above checking methods provided by models. Class variables are provided in the following table. 
        The STS document contains more information
        """
        if not all(isinstance(x, str) for x in self.bcnTag):
            raise Exception("Incorrect data type: bcnTag must be a list of strings")

        if not all(isinstance(x, float) for x in self.recurVarValue):
            raise Exception("Incorrect data type: recurVarValue must be a list of floats")

        if not all(isinstance(x, float) for x in self.quantVarValue):
            raise Exception("Incorrect data type: quantVarValue must be a list of floats")
        
        # (*) If blank, reports blank.
        if self.quantUnit == "":
            logger.warning('Warning: %s', 'The quantity unit supplied is blank.', extra=d)
        return 


    def updateObject(self, varName, newValue):
    	"""Purpose: Use parameters to change BCN variale value.
    	"""
    	self.bcnName[varName] = newValue 
    	return 


    # Below methods were commented out, due to updates to Psuedocode document 5. BCN Class
    """
	def updateSensFlows(newSensFlowNonDisc, newSensFlowDisc, newSensFlowQuant):
		Purpose: Updates sensitivity flows with the input flows
		pass

	def updateUncFlows(newUncFlowNonDisc, newUncFlowDisc, newUncFlowQuant):
		Purpose: Updates uncertainty flows with input flows
		pass
	"""