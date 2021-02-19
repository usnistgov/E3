from django.db import models
from ../../libraries import discounting
class Analysis(models.Model):
    
    """
    Purpose: Creates and validates Analysis objects.
    """
    # Verify data type and length as Alternative object is created.
    alternativeID = models.IntegerField()
    alternativeName = models.CharField(max_length=30)
    #alternativeBCNList = models.List
    baselineBool = models.BooleanField(max_length=30)

    #def __init__(self):
    
    def validateAlternativeObject(objectList):
        for bcnObject in objectList.bcnObject:
            for x in bcnObject:
                if not x.bcnID:
                    raise Exception("BcnID does not exist for one or more BCN Objects")
                # check all bcnID reference existing BCN objects.
                # check only one alternative has baselineBool = True

        return 