sys.path.insert(1, '/e3_django/main/libraries')
import cashFlow

class TotalRequiredFlows(models.Model):
    """
    Purpose: Stores total flows for a single Alternative.
    """
    # Verify data type and length as Object is created.
    altID = models.IntegerField()
    sensBool = models.BooleanField(default=False)
    uncBool = models.BooleanField(default=False)

    totCostNonDisc  = models.JSONField()
	totCostDisc  = models.JSONField()
	totCostNonDiscInv  = models.JSONField()
	totCostDiscInv  = models.JSONField()
	totCostNonDiscNonInv  = models.JSONField()
	totCostDiscNonInv  = models.JSONField()
	totBenefitsNonDisc  = models.JSONField()
	totBenefitsDisc  = models.JSONField()
	totCostDir  = models.JSONField()
	totCostInd  = models.JSONField()
	totCostExt  = models.JSONField()
	totCostDirDisc  = models.JSONField()
	totCostIndDisc  = models.JSONField()
	totCostExtDisc  = models.JSONField()
	totBenefitsDir  = models.JSONField()
	totBenefitsInd  = models.JSONField()
	totBenefitsExt  = models.JSONField()
	totBenefitsDirDisc  = models.JSONField()
	totBenefitsIndDisc  = models.JSONField()
	totBenefitsExtDisc  = models.JSONField()

    def __init__(self):
	    # TODO: Need to check that JSONFields are list of 'floats'.
	    

	@classmethod
    def __init__(self):
        """
        Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
        in addition to the above checking methods provided by models. Class variables are provided in the following table. 
        The STS document contains more information
        """
        for var in [totCostNonDisc, totCostDisc, totCostNonDiscInv, totCostDiscInv, totCostNonDiscNonInv, totCostDiscNonInv, \
         totBenefitsNonDisc, totBenefitsDisc, totCostDir, totCostInd, totCostExt, totCostDirDisc, totCostIndDisc, totCostExtDisc \
         totBenefitsDir, totBenefitsInd, totBenefitsExt, totBenefitsDirDisc, totBenefitsIndDisc, totBenefitsExtDisc]:

	        if not all(isinstance(x, int) for x in self.var):
	            raise Exception("Incorrect data type Error. Check your inputs are floats")



	def addFlow(flowName, flow):
		"""
		Purpose: Based on provided flowName, adds the flow to the appropriate variable. 

		Note: flowName must be a string with the same name as the variable, 
		without the enclosing brackets.
		"""
		pass

	def updateFlow(flowName, flow):
		"""
		Purpose: Based on provided flowName, resets current flow to the input flow.

		Note: flowName must be a string with the same name as the variable,
		without the enclosing brackets.

		"""
		pass

	def updateAllFlows(flowsList):
		"""
		Purpose: Updates all flows in the flowList simultaneously.

		Note: Input order is the same as order that variables appear in the object.
		"""
		pass

