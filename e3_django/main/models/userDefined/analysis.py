from django.db import models
sys.path.insert(1, '/e3_django/main/libraries')
import (validateRead, cashFlow, discounting)

class Analysis(models.Model):
    """
    Purpose: Creates and validates Analysis objects.
    """
    # Verify data type and range as Analysis object is created (In addition to var check in __init__)
    analysisType = models.CharField(max_length=30, blank=True) # blank=True refers to unrequired var.
    projectType = models.CharField(max_length=30)
    objToReport = models.JSONField(blank=True) # further check in __init__ constructor. See below
    studyPeriod = models.IntegerField(blank=True, validators = [MinValueValidator(0)])
    baseDate = models.DateTimeField(auto_now_add=True, blank=True)
    serviceDate = models.DateTimeField(auto_now_add=True) # Must be later than Base Date
    timestepVal = models.CharField(max_length=30, blank=True, validators=[MinValueValidator(self.baseDate)])
    timestepComp = models.IntegerField(blank=True, validators=[MaxValueValidator(self.studyPeriod), MinValueValidator(0)]) # Must be positive and less than study period
    outputRealBool = models.BooleanField(blank=True)
    interestRate = models.DecimalField(max_digits=7, decimal_places=2) # May add check later that they're positive
    dRateReal = models.DecimalField(max_digits=7, decimal_places=2, blank=True) # May add check later that they're positive
    dRateNom = models.DecimalField(max_digits=7, decimal_places=2) # May add check later that they're positive
    inflationRate = models.DecimalField(max_digits=7, decimal_places=2) # May add check later that they're positive
    Marr = models.DecimalField(max_digits=7, decimal_places=2, blank=True) # May add check later that they're positive
    reinvestRate = models.DecimalField(max_digits=7, decimal_places=2, blank=True) # May add check later that they're positive
    incomeRateFed = models.DecimalField(max_digits=7, decimal_places=2)
    incomeRateOther = models.DecimalField(max_digits=7, decimal_places=2)
    #noAlt = models.IntegerField(validators = [MinValueValidator(1)]) # Included in second table (of Pseudocode 4. Analysis Class), but not in first table. Omitted for now
    #baseAlt = models.IntegerField() # Included in second table (of Pseudocode 4. Analysis Class), but not in first table. Omitted for now 
    location = models.JSONField() # further check in __init__ constructor. See below


    @classmethod
    """
    Purpose: Standard class constructor method. Create object based off of list of inputs developed from json string
    in addition to the above checking methods provided by models. Class variables are provided in the following table. 
    The STS document contains more information
    """
    def __init__(self):
        if not all(isinstance(x, str) for x in self.objToReport):
            raise Exception("Incorrect data type: objToReport must be a list of strings")

        if not all(isinstance(x, float) for x in self.location):
            raise Exception("Incorrect data type: Location must be a list of strings")
        return
 

    # Below method was checked upon Object creation, see above.
    """ 
    def validateAnalysisObject(analysisObj):
        Purpose: Verifies that all inputs are correct required type, and in valid ranges
        Note: Will verify as the object is created, see above
    """


    def validateDiscountRate(self):
        discount_rate_vars = [self.dRateReal, self.dRateNom, self.inflationRate, self.outputRealBool]

        # If outputRealBool is True, and dRateReal & inflationRate is given
        if (self.outputRealBool and self.dRateReal and self.inflationRate) or \
            # OR if outputRealBool is False, and dRateReal & inflationRate is given
            (not self.outputRealBool and self.dRateNom and self.inflationRate):
            pass


        # If outputReal is True, and dRateNom & dRateReal is given
        elif dRateNom and dRateReal and outputRealBool:
            # Use dRateReal here
            if not inflationRate: 
                # Update inputObjList with computed inflation rate
                inputObjList = discounting.inflationRateCalc(dRateNom, dRateReal)

                logger.warning('Warning: %s', 'Both the Real and Nominal discount rate were provided \
                    based on User input. Only the Real rate will be used in calculations', extra=d)
                
                return inputObjList


        # If outputRealBool is False, and dRateNom & dRateReal is given
        elif dRateNom and dRateReal and not outputRealBool:
            # Use dRateNom
            if not inflationRate:
                # Update inputObjList with computed inflation rate
                inputObjList = discounting.inflationRateCalc(dRateNom, dRateReal)

                logger.warning('Warning: %s', 'Both the Real and Nominal discount rate were provided \
                    based on User input. Only the Nominal rate will be used in calculations', extra=d)
                
                return inputObjList

        
        # If outputRealBool is True, and dRateNom & inflationRate is given
        elif outputRealBool and dRateNom and inflationRate:
            # Update inputObjList with computed real rate
            inputObjList = discounting.dRateRealCalc(dRateNom, inflationRate)

            logger.warning('Warning: %s', 'Output defined as Real but Nominal rate provided, Real \
                rate has been calculated from available inputs and will be used in subsequent calculations')
            
            return inputObjList


        # If outputRealBool is False, and dRateNom & inflationRate is given
        elif not outputRealBool and dRateReal and inflationRate:
            # Update inputObjList with computed nominal rate
            inputObjList = discounting.dRateNomCalc(dRateReal, inflationRate)

            logger.warning('Warning: %s', 'Output defined as Nominal but Real rate provided, Nominal \
                rate has been calculated from available inputs and will be used in subsequent calculations')
            
            return inputObjList
        

        # If outputRealBool is True, dRateReal is given, but inflationRate does not exist
        elif outputRealBool and dRateReal and not inflationRate:
            # Call to discounting library
            return
            
        return


