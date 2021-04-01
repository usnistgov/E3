from django.db import models
from main.libraries import validateRead
from main.models import sensitivitySummary
"""
from rest_framework.serializers import Serializer, FileField

# Serializers define the API representation
class UploadSerializer(Serializer):
    file_uploaded = FileField()
    class Meta:
        fields = ['file_uploaded']

"""

class Sensitivity(models.Model):
    """
    Purpose: Stores total flows for a single BCN.
    """
    # Verify data type and range as BCN object is created (In addition to var check in __init__)
    globalVarBool = models.BooleanField(blank=True)
    altID = models.IntegerField(unique=True, blank=True) # not required if globalVarBool is false
    bcnID  = models.CharField(max_length=30, blank=True, default='') # not required if globalVarBool is false
    varName = models.CharField(max_length=30, blank=True, default='')
    diffType = models.CharField(max_length=30, blank=True, default='')
    diffVal = models.DecimalField(max_digits=7, decimal_places=2)
	
    @classmethod
    def __init__(self):
        """
        Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
        in addition to the above checking methods provided by models. Class variables are provided in the following table. 
        The STS document contains more information
        """
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
