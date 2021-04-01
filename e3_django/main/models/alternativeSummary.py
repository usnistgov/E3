from main.libraries import cashFlow
from .userDefined import bcn
from django.db import models

class AlternativeSummary(models.Model):
    """
    Purpose: Stores total cash flows for a single altID-tag combination.
    """
    # Verify data type and range as Object is created.
    """ TODO: 
    altID 
	totalBenefits
	totalCosts
	totalCostsIn
	totalCostsNonInv
	netBenefits
	netSaviings
	SIR
	IRR = # optional
	AIRR = 
	SPP = 
	SPP = 
	BCR = 
	quantSum = models.JSONField()
	quantUnits – list of strings ith index is the unit for the ith element in quantSum
	MARR – taken directly from Analysis object
	"""
    deltaQuant = models.JSONField()
    nsDeltaQuant = models.JSONField()
    nsPercQuant = models.JSONField()
    nsElasticityQuant = models.JSONField()


    @classmethod
    def __init__(self):
        self.bcnType = bcn.bcnType # bcn.bcnType variable stored here for convenience
        self.bcnSubType = bcn.bcnSubType # bcn.bcnSubType variable stored here for convenience
		
        if not all(isinstance(x, float) for x in self.quantSum):
            raise Exception("Incorrect data type: quantSum must be a list of floats")
        
        if not all(isinstance(x, float) for x in self.deltaQuant):
            raise Exception("Incorrect data type: deltaQuant must be a list of floats")

        if not all(isinstance(x, float) for x in self.nsDeltaQuant):
            raise Exception("Incorrect data type: nsDeltaQuant must be a list of floats")

        if not all(isinstance(x, float) for x in self.nsPercQuant):
            raise Exception("Incorrect data type: nsPercQuant must be a list of floats")

        if not all(isinstance(x, float) for x in self.nsElasticityQuant):
            raise Exception("Incorrect data type: nsElasticityQuant must be a list of floats")

        return



    def updateMeasure(self, measureName, flow):
		# Based on measureName (string with the exact same name as the variable without 
		# the enclosing brackets if they exist) reset current measure to the input measure.
		# ?: which variable orresponds to this?

		# self.x = flow
        return
