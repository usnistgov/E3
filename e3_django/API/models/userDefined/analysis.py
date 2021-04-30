from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Analysis(models.Model):
	"""
	Purpose: Initializes an Analysis object
	"""
	analysisType 	= models.CharField(max_length=30, null=True)
	projectType 	= models.CharField(max_length=30)
	objToReport		= models.JSONField(null=True, default=dict)
	studyPeriod 	= models.IntegerField(null=True, validators=[MinValueValidator(0)])
	baseDate 		= models.DateTimeField(null=True)
	serviceDate 	= models.DateTimeField()
	timestepVal		= models.CharField(max_length=30, null=True, validators=[MinValueValidator(baseDate)])
	timestepComp	= models.IntegerField(null=True, validators=[MaxValueValidator(studyPeriod), MinValueValidator(0)])
	outputRealBool	= models.BooleanField(null=True)
	interestRate 	= models.DecimalField(max_digits=7, decimal_places=2) # May add check later that they're positive
	dRateReal		= models.DecimalField(max_digits=7, decimal_places=2, null=True) # May add check later that they're positive
	dRateNom		= models.DecimalField(max_digits=7, decimal_places=2) # May add check later that they're positive
	inflationRate	= models.DecimalField(max_digits=7, decimal_places=2) # May add check later that they're positive
	Marr			= models.DecimalField(max_digits=7, decimal_places=2, null=True) # May add check later that they're positive
	reinvestRate	= models.DecimalField(max_digits=7, decimal_places=2, null=True) # May add check later that they're positive
	incomeRateFed	= models.JSONField(null=True, default=list)
	incomeRateOther	= models.JSONField(null=True, default=list)
	location		= models.JSONField(null=True, default=dict)


	def validateDiscountRate(self):
		discount_rate_vars = [self.dRateReal, self.dRateNom, self.inflationRate, self.outputRealBool]

		# If outputRealBool is True, and dRateReal & inflationRate is given, OR if outputRealBool is False, and dRateReal & inflationRate is given
		if (self.outputRealBool and self.dRateReal and self.inflationRate) or \
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
