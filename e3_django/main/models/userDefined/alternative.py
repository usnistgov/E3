from django.db import models
sys.path.insert(1, '/e3_django/main/libraries')
import validateRead
from .. import AlternativeSummary

class Analysis(models.Model):
    """
    Purpose: Creates and validates Analysis objects.
    """
    # Verify data type and length as Alternative object is created.
    alternativeID = models.IntegerField(blank=False)
    alternativeName = models.CharField(max_length=30, blank=False)
    alternativeBCNList = models.JSONField()
    baselineBool = models.BooleanField()


    @classmethod
    def __init__(self):
        """
        Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
        in addition to the above checking methods provided by models. Class variables are provided in the following table. 
        The STS document contains more information
        """
        if not all(isinstance(x, int) for x in self.alternativeBCNList):
            raise Exception("Incorrect data type: alternativeBCNList must be a list of unique integers")
        # TODO:  Check that self.alternativeBCNList is a list of bcnIDs associated with the alternativeID (required)
        return 

    
    def validateAlternativeObject(objectList):
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