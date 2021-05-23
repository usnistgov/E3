from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import logging

logger = logging.getLogger(__name__)

class BCN(models.Model):
    """
    Purpose: Initializes a BCN object, verifies data fields.
    """
    bcnID         = models.IntegerField(unique=True)
    altID         = models.JSONField(null=False, default=list)
    bcnType       = models.CharField(null=False, max_length=30)
    bcnSubType    = models.CharField(null=True, max_length=30)
    bcnName       = models.CharField(null=True, max_length=30)
    bcnTag        = models.JSONField(null=True, default=list) 
    initialOcc    = models.IntegerField(null=True, validators=[MinValueValidator(0)]) 
    rvBool        = models.BooleanField(null=True)
    bcnRealBool   = models.BooleanField(null=True)
    bcnInvestBool = models.BooleanField(null=True)
    bcnLife       = models.IntegerField(null=True, validators=[MinValueValidator(1)]) 
    recurBool     = models.BooleanField(null=False)
    recurInterval = models.IntegerField(null=True, validators=[MinValueValidator(1)])
    recurVarRate  = models.CharField(null=True, max_length=30)
    recurVarValue = models.JSONField(null=True, default=list) 
    recurEndDate  = models.DateTimeField(null=True, auto_now_add=True, validators=[MinValueValidator(initialOcc)]) 
    valuePerQ     = models.DecimalField(null=True, max_digits=7, decimal_places=2)
    quant         = models.DecimalField(null=False, max_digits=7, decimal_places=2)
    quantVarRate  = models.CharField(null=True, max_length=30) 
    quantVarValue = models.JSONField(null=True) 
    quantUnit     = models.CharField(null=True, max_length=30, default='dollars') 

    
    def __init__(self, *args, **kwargs):
        """ 
        Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
        in addition to the above checking methods provided by models. Class variables are provided in the following table. 
        The STS document contains more information
        """
        print("BCN CONSTRUCTOR method called")
        # Add anything that should run BEFORE model validation.
        return super().__init__(*args, **kwargs)


    def validateBCNObject(self, objectList):
        """
        Purpose: Verifies that all inputs are correct required data types and in valid range. 
		Note: Does NOT actually create or return the BCN object.
		Return: null
        """
        obj = objectList.bcnObject
        try:
            BCN.objects.create(bcnID=obj.bcnID, altID=obj.altID, bcnType=obj.bcnType, bcnSubType=obj.bcnSubType, bcnName=obj.bcnName, \
                bcnTag=obj.bcnTag, initialOcc=obj.initialOcc, rvBool=obj.rvBool, bcnRealBool=obj.bcnRealBool, bcnInvestBool=obj.bcnInvestBool, \
                bcnLife=obj.bcnLife, recurBool=obj.recurBool, recurInterval=obj.recurInterval, recurVarRate=obj.recurVarRate, recurVarValue=obj.recurVarValue, \
                recurEndDate=obj.recurEndDate, valuePerQ=obj.valuePerQ, quant=obj.quant, quantVarRate=obj.quantVarRate, quantVarValue=obj.quantVarValue, \
                quantUnit=obj.quantUnit)
            # Check here that initialOcc occurs at valid timestep
            # Check here that initialOcc is less than studyPeriod
            # Check here that recurEndDate is less than studyPeriod

            if not all(isinstance(x, str) for x in obj.bcnTag):
                logger.error("Err: %s", "all elements in bcnTag field must be of string type.")

            if not all(isinstance(x, float) for x in obj.recurVarValue):
                logger.error("Err: %s", "all elements in recurVarValue field must be of float type.")

            if not all(isinstance(x, float) for x in obj.quantVarValue):
                logger.error("Err: %s", "all elements in quantVarValue field must be of float type.")

            # Based on chosen bcnType, check that all required inputs are included.
            if self.bcnType == 'Benefit':
                print("BCN is of 'Benefit' type.")
                # Check required fields for Benefit
                if not self.initialOcc or not self.bcnRealBool or not self.valuePerQ:
                    logger.error("Err: %s", "Invalid input(s) for BCN object using 'Benefit' type. \
                    Check that you have supplied all necessary fields: initialOcc, bcnRealBool, valuePerQ.")

                # Check optional fields for Benefit
                if not self.quantUnit:
                    logger.info("Note: %s", "Since quantUnit was not provided, value will be assumed to be in dollars.")
            
            elif self.bcnType == 'Cost':
                print("BCN is of 'Cost' type. Negative cost refers to Revenue.")
                # Check required fields for Cost
                if not self.bcnRealBool or not self.bcnInvestBool or not self.valuePerQ:
                    logger.error("Err %s", "Invalid input(s) for BCN object using 'Cost' type. \
                    Check that you have supplied all necessary fields: bcnRealBool, bcnInvestBool, valuePerQ.")

                # Check optional fields for Cost
                if not self.quantUnit:
                    logger.info("Note: %s", "Since quantUnit is not provided, value will be assumed to be in dollars.")    

            elif self.bcnType == 'NonMonetary':
                print("BCN is of 'NonMonetary' type.")
            # Check required fields for NonMonetary
                if not self.bcnTag or not self.quantUnit:
                    logger.error("Err %s", "Invalid input(s) for BCN object using 'NonMonetary' type. \
                    Check that you have supplied the field: 'bcnTag', 'quantUnit' required for non-monetary to simplify measure calculations.")

            else:
                logger.error("Err: BCN type is of unknown type")

            # Check conditional fields 
                if self.recurBool:
                    if not self.recurInterval or not self.recurVarRate or not self.recurVarValue:
                        logger.error("Err: %s", "Invalid input(s) for BCN object where 'recurBool' is True. \
                        Check that you have supplied all necessary fields: recurInterval, recurVarRate, recurVarValue.")
                if self.quantVarRate:
                    if not self.quantVarValue:
                        logger.error("Err: %s", "Invalid input(s) for BCN object where 'quantVarRate' exists. \
                        Check that you have supplied the field: quantVarValue.")

        except:
            logger.error("Err: %s", "Invalid input for BCN object. Check that they are correct data type and in range.")

        # Check optional fields 
        if not self.recurEndDate:
            logger.info("Note: %s", "Since recurEndDate is not provided, BCN will occur for the entire study period.")

        # (*) If blank, reports blank.
        if self.quantUnit == "":
            logger.warning('Warning: %s', 'The quantity unit supplied is blank.', extra=d)

        print("All inputs checked and verified. If no Err messages, BCN object can be created.")
        
        return


    def updateObject(self, varName, newVal):
        """
        Purpose: Updates BCN 'varName' variable value to 'newVal'.
        """
        self.varName = newVal
        logger.info("Success: BCN variable %s was updated to %s.", varName, newVal)

        return
