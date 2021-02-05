from django.db import models
from .. .. import libraries.discounting
class Analysis(models.Model):
    """
    Purpose: Creates and validates Analysis objects.
    
    Parameters:
    Returns:
    """

    # Verify data type and length as Analysis object is created.
    analysisType = models.CharField(max_length=30)
    projectType = models.CharField(max_length=30)
    objToReport = models.CharField(max_length=30)
    studyPeriod = models.IntegerField()
    baseDate = models.DateTimeField(auto_now_add=True)
    serviceDate = models.DateTimeField(auto_now_add=True)
    timestepVal = models.CharField(max_length=30)
    timestepComp = models.IntegerField()
    outputRealBool = models.BooleanField(default=False)
    interestRate = models.DecimalField(max_digits=7, decimal_places=2)
    dRateReal = models.DecimalField(max_digits=7, decimal_places=2)
    dRateNom = models.DecimalField(max_digits=7, decimal_places=2)
    inflationRate = models.DecimalField(max_digits=7, decimal_places=2)
    Marr = models.DecimalField(max_digits=7, decimal_places=2)
    reinvestRate = models.DecimalField(max_digits=7, decimal_places=2)
    incomeRateFed = models.DecimalField(max_digits=7, decimal_places=2)
    incomeRateOther = models.DecimalField(max_digits=7, decimal_places=2)
    noAlt = models.IntegerField()
    # location =  
    # ?: How to check if data field is a list?

    #@classmethod
    #def

    """ validateAnalysisObject(analysisObj):
    Will verify as the object is created, see above
    """

    def validateDiscountRate(self):
        discount_rate_vars = [dRateReal, dRateNom, inflationRate, outputRealBool]
        if (outputRealBool and dRateReal and inflationRate) or \
            (not outputRealBool and dRateNom and inflationRate):
            pass
        
        elif dRateNom and dRateReal and outputRealBool:
            # using dRateReal
            if not inflationRate:
                # Update inputObjList with computed inflation rate
                inputObjList = discounting.inflationRateCalc(dRateNom, dRateReal)
                logger.warning('Warning: %s', 'Both the Real and Nominal discount rate were provided \
                    based on User input. Only the Real rate will be used in calculations', extra=d)
                return inputObjList

        elif dRateNom and dRateReal and not outputRealBool:
            # using dRateNom
            if not inflationRate:
                # Update inputObjList with computed inflation rate
                inputObjList = discounting.inflationRateCalc(dRateNom, dRateReal)
                logger.warning('Warning: %s', 'Both the Real and Nominal discount rate were provided \
                    based on User input. Only the Nominal rate will be used in calculations', extra=d)
                return inputObjList
        
        elif outputRealBool and dRateNom and inflationRate:
            # Update inputObjList with computed real rate
            inputObjList = discounting.dRateRealCalc(dRateNom, inflationRate)
            logger.warning('Warning: %s', 'Output defined as Real but Nominal rate provided, Real \
                rate has been calculated from available inputs and will be used in subsequent calculations')
            return inputObjList

        elif not outputRealBool and dRateReal and inflationRate:
            # Update inputObjList with computed nominal rate
            inputObjList = discounting.dRateNomCalc(dRateReal, inflationRate)
            logger.warning('Warning: %s', 'Output defined as Nominal but Real rate provided, Nominal \
                rate has been calculated from available inputs and will be used in subsequent calculations')
            return inputObjList
        
        elif outputRealBool and dRateReal and not inflationRate:
            # call Discounting library

            return
            
        return


