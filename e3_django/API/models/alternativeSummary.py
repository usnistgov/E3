from django.db import models
import logging

from django.db.models import DecimalField

logger = logging.getLogger(__name__)

MAX_DIGITS = 20
DECIMAL_PLACES = 5

class AlternativeSummary(models.Model):
	"""
	Purpose: Stores total cash flows for a single altID-tag combination. Verify data type and range as Object is created. 
	"""
	altID 			 	= models.JSONField(default=list, unique=True)
	totalBenefits	 	= models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) 
	totalCosts 		 	= models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) 
	totalCostsInv	 	= models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) 
	totalCostsNonInv 	= models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) 
	netBenefits		 	= models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) 
	netSavings 	 		= models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
	SIR 			 	= models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) 
	IRR 			 	= models.DecimalField(null=True, max_digits=MAX_DIGITS, decimal_places=3) #optional
	AIRR 			 	= models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
	DPP 			 	= models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
	SPP 			 	= models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) 
	BCR 			 	= models.DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) 
	quantSum 		 	= models.JSONField(default=list) 
	quantUnits 		 	= models.JSONField(default=list) #TODO: Check list of strings; the ith index is the unit for ith element in quantSum
	MARR  			 	= DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES) #taken directly from Analysis object
	deltaQuant 			= models.JSONField(default=list)
	nsDeltaQuant 		= models.JSONField(default=list)
	nsPercQuant 		= models.JSONField(default=list)
	nsElasticityQuant 	= models.JSONField(default=list)


	def __init__(self, *args, **kwargs):
		"""
		Purpose: Standard class constructor method. Create object based off list of inputs and developed from json string
		in addition to the above checking methods provided by Django models. Class variables are provided in the following table.
		The STS document contains more information.
		"""
		print("AlternativeSummary constructor method called.")

		self.bcnType = bcn.bcnType # bcn.bcnType variable stored here for convenience
		self.bcnSubType = bcn.bcnSubType # bcn.bcnSubType variable stored here for convenience
		return super().__init__(*args, **kwargs)
		

	def validateAlternativeSummaryObject(self, objectList):
		obj = objectList.alternativeSummaryObject 
		try:
			AlternativeSummary.objects.create(altID=obj.altID, totalBenefits=obj.totalBenefits, totalCosts=obj.totalCosts, 
			totalCostsIn=obj.totalCostsIn, totalCostsNonInv=obj.totalCostsNonInv, netBenefits=obj.netBenefits, netSaviings=obj.netSaviings,
			SIR=obj.SIR, IRR=obj.IRR, AIRR=obj.AIRR, DPP=obj.DPP SPP=obj.SPP, BCR=obj.BCR, quantSum=obj.quantSum, quantUnits=obj.quantUnits, Marr=obj.Marr,
			deltaQuant=obj.deltaQuant, nsDeltaQuant=obj.nsDeltaQuant, nsPercQuant=obj.nsPercQuant, nsElasticityQuant=obj.nsElasticityQuant
			)

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
		except:
			logger.error("Error: %s", "Invalid input for AlternativeSummary object. Check that they are correct data type.")

		print("All inputs checked and verified. If no Err messages, AlternativeSummary object can be created.")
		return


	def updateMeasure(measureName, flow):
		"""
		Purpose: Based on measureName (string with the exact same name as the variable without 
		the enclosing brackets if they exist) reset current measure to the input measure.
		"""

		# if variable with name `measureName` exists, reset current measure with input flow.
		if self.measureName:
    			self.measureName = flow
		return
