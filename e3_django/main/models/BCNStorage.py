sys.path.insert(1, '/e3_django/main/libraries')
import cashFlow

class BCNStorage(models.Model):
    """
    Purpose: Stores total cash flows for a single altID-tag combination.
    """
    # Verify data type and length as Object is created.
    bcnName = models.CharField(max_length=30)
    bcnID = models.IntegerField(blank=False)
    altID = models.BooleanField()
    bcnType =  models.CharField(max_length=30) # Name changed from type -> bcnType due to reserved Python variable
    subType =  models.CharField(max_length=30) # Equivalent to bcn.subtype for bcnID
    tag =  models.CharField(max_length=30) # Equivalent to bcn.tag for bcnID
    bcnNonDiscFlow = models.JSONField()
    bcnDiscFlow = models.JSONField()
    quantList = models.JSONField()
    quantUnt = models.CharField(max_length=30, blank=False)
    sensBool  = models.BooleanField()
    sensFlowNonDisc = models.JSONField()
    sensFlowDisc = models.JSONField()
    sensQuantList = models.JSONField()
    uncBool = models.BooleanField()
    uncFlowNonDisc = models.JSONField()
    uncFlowDisc = models.JSONField()
    uncQuantList = models.JSONField()
    # further check in __init__ constructor. See below


    @classmethod
    def __init__(self):
        """
        Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
        in addition to the above checking methods provided by models. Class variables are provided in the following table. 
        The STS document contains more information
        """
        if not all(isinstance(x, int) for x in self.altID):
            raise Exception("Incorrect data type: altID must be a list of unique integers")
        
        if not all(isinstance(x, float) for x in self.bcnNonDiscFlow):
            raise Exception("Incorrect data type: bcnNonDiscFlow must be a list of unique floats")
        
        if not all(isinstance(x, float) for x in self.bcnDiscFlow):
            raise Exception("Incorrect data type: bcnDiscFlow must be a list of unique floats")
        
        if not all(isinstance(x, float) for x in self.quantList):
            raise Exception("Incorrect data type: quantList must be a list of unique floats")
        
        if not all(isinstance(x, int) for x in self.sensFlowNonDisc):
            raise Exception("Incorrect data type: sensFlowNonDisc must be a list of unique integers")
        
        if not all(isinstance(x, float) for x in self.sensFlowDisc):
            raise Exception("Incorrect data type: sensFlowDisc must be a list of unique floats")
        
        if not all(isinstance(x, float) for x in self.sensQuantList):
            raise Exception("Incorrect data type: sensQuantList must be a list of unique floats")
        
        if not all(isinstance(x, float) for x in self.uncFlowNonDisc):
            raise Exception("Incorrect data type: uncFlowNonDisc must be a list of unique floats")
        
        if not all(isinstance(x, float) for x in self.uncFlowDisc):
            raise Exception("Incorrect data type: uncFlowDisc must be a list of unique floats")
        
        if not all(isinstance(x, float) for x in self.uncQuantList):
            raise Exception("Incorrect data type: uncQuantList must be a list of unique floats")
        return 


	def updateSensFlows(self, newSensFlowNonDisc, newSensFlowDisc, newSensFlowQuant):
        # TODO: Updates the sensitivity flows with the input flows
        return

    def updateUncFlows(self, newUncFlowNonDisc, newUncFlowDisc, newUncFlowQuant):
        # TODO: Updates the uncertainty flows with input flows
        return
