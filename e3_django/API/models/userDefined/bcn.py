from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class BCN(models.Model):
    """
    Purpose: Initializes a BCN object
    """
    bcnID         = models.IntegerField(null=True, unique=True)
    altID         = models.JSONField(null=True, default=list)
    bcnType       = models.CharField(null=True, max_length=30)
    bcnSubType    = models.CharField(max_length=30)
    bcnName       = models.CharField(max_length=30)
    bcnTag        = models.JSONField() 
    initialOcc    = models.IntegerField(null=True, validators=[MinValueValidator(0)]) # TODO: Check that this occurs at a valid timestep, check that value is less than studyPeriod.
    rvBool        = models.BooleanField()
    bcnRealBool   = models.BooleanField(null=True)
    bcnInvestBool = models.BooleanField(null=True)
    #! Check: Input JSON has a missing field, but docs require field.
    bcnLife       = models.IntegerField(null=True, validators=[MinValueValidator(1)]) 
    recurBool     = models.BooleanField(null=True)
    recurInterval = models.IntegerField(null=True, validators=[MinValueValidator(1)])
    recurVarRate  = models.CharField(null=True, max_length=30)
    recurVarValue = models.JSONField(null=True) # Included in third table (of Pseudocode 5. BCN Class), but not in first table; Omitted for now
    recurEndDate  = models.DateTimeField(auto_now_add=True, validators=[MinValueValidator(initialOcc)]) # TODO: check that value is less than studyPeriod.
    valuePerQ     = models.DecimalField(null=True, max_digits=7, decimal_places=2)
    quant         = models.DecimalField(null=True, max_digits=7, decimal_places=2)
    quantVarRate  = models.CharField(null=True, max_length=30) # Docs say this is required, but input JSON misses this field
    quantVarValue  = models.JSONField(null=True)
    quantUnit     = models.CharField(null=True, max_length=30) # If blank, report blank? See (*) line 

    """ 
    @classmethod
    Put the code in 'master' here
    """

    def updateObject(varName, newValue):
        """
        Purpose: use parameters to change BCN variable value.
        """
        self.bcnName[varName] = newValue
        return

    """
    def updateSensFlows(newSenseFlowNonDisc, newSensFlowDisc, newSensFlowQuant):
        Purpose: Updates sensitivity flows with the input flows
        pass

    def updateUncFlows(newUncFlowNonDisc, newUncFlowDisc, newUncFlowQuant):
        Puspose: Updates uncertainty flows with input flows
        pass
    """