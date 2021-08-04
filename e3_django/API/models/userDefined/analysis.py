from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from API.libraries import discounting
import logging
import math

logger = logging.getLogger(__name__)

class Analysis(models.Model):

	def validateAnalysisObject(self, objectList):
		"""
		Purpose: Verifies that all inputs are correct required data types and in valid range. 
		Note: Does NOT actually create or return the Analysis object.
		Return: null
		"""
		obj = objectList.analysisObject
		try:
			Analysis.objects.create(analysisType=obj.analysisType, projectType=obj.projectType, objToReport=obj.objToReport, \
				studyPeriod=obj.studyPeriod, baseDate=obj.baseDate, serviceDate=obj.serviceDate, timestepVal=obj.timestepVal, \
				timestepComp=obj.timestepComp, outputRealBool=obj.outputRealBool, interestRate=obj.interestRate, dRateReal=obj.dRateReal, \
				dRateNom=obj.dRateNom, reinvestRate=obj.reinvestRate, incomeRateFed=obj.incomeRateFed, incomeRateOther=obj.incomeRateOther, 
				location=obj.location)

			if not all(isinstance(x, str) for x in obj.objToReport):
				logger.error("Err: %s", "all elements in objToReport field must be of string type.")

			if not all(isinstance(x, str) for x in obj.location):
				logger.error("Err: %s", "all elements in location field must be of string type.")


			# Based on chosen analysisType, check that all required inputs are included.
			if self.analysisType == 'LCCA':
				print("Analysis type is LCCA.")
				# Check here that all required inputs for LCCA is included. Else, raise Err: Invalid input for Analysis object using 'LCCA' type.
				
			elif self.analysisType == 'BCA':
				print("Analysis type is BCA")
				# Check here that all required inputs for BCA is included. Else, raise Err: Invalid input for Analysis object using 'BCA' type.

			elif self.analysisType == 'Cost-Loss':
				print("Analysis type is Cost-Loss")
				# Check here that all required inputs for Cost-Loss is included. Else, raise Err: Invalid input for Analysis object using 'Cost-Loss' type.

			elif self.anslysisType == 'Profit Maximization':
				print("Analysis type is profit Maximization")
				# Check here that all required inputs for Profit Maximization is included. Else, raise Err: Invalid input for Analysis object using 'Profit Maximization' type.

			else:
				logger.info("Analysis type is default")

		except:
			logger.error("Error: %s", "Invalid input for Analysis object. Check that they are correct data type and in range.")

		print("All inputs checked and verified. If no Err messages, Analysis object can be created.")

		return
    

	def validateDiscountRate(self):
		"""
		Purpose: Validates that discounted rates are adjusted for in the Analysis object.
		"""
		inputObjectList = [self.dRateReal, self.dRateNom, self.inflationRate, self.outputRealBool]

		# If outputRealBool is True, and dRateReal & inflationRate is given, OR if outputRealBool is False, and dRateReal & inflationRate is given
		if (self.outputRealBool and self.dRateReal and self.inflationRate and not self.dRateNom) or \
		(not self.outputRealBool and self.dRateNom and self.inflationRate and not self.dRateReal):
			return True

		# If outputReal is True, and dRateNom & dRateReal is given
		elif (self.outputRealBool and self.dRateReal and self.inflationRate and self.dRateNom) or \
			(not self.outputRealBool and self.dRateNom and self.inflationRate and self.dRateReal):
			inflRateCalc = discounting.inflationRateCalc(self.dRateNom, self.dRateReal)
			if math.abs(inflRateCalc - self.inflationRate) > 0.01: # if inflRateCalc is NOT within tolerance (start at 1%, adjust as needed)
				return "Inflation rate calculated from nominal and real rate does NOT match the provided inflation rate. \
					Calculation with the provided rate used in calculation may not be correct."
			else:
				return True
		
		elif self.outputRealBool and self.dRateNom and self.dRateReal:
			# use dRateReal
			if not self.inflationRate:
				# Update inputObjectList with calculated inflationRate
				inputObjectList[2] = discounting.inflationRate(self.dRateNom, self.dRateReal)
				
				logger.warning("Warning: %s", "Both the Real and Nominal discount rates were provided based on User input. \
				Only the Real rate will be used in calculations.")
				return inputObjectList

		elif self.outputRealBool and self.dRateNom and self.dRateReal:
			# use dRateNom
			if not self.inflationRate:
    			# Update inputObjectList with calculated inflationRate
				inputObjectList[2] = discounting.inflationRate(self.dRateNom, self.dRateReal)
				
				logger.warning("Warning: %s", "Both the Real and Nominal discount rates were provided based on User input. \
				Only the Nominal rate will be used in calculations.")
				return inputObjectList

		elif self.outputRealBool and self.dRateNom and self.inflationRate:
			realRate = discounting.dRateRealCalc(self.dRateNom, self.inflationRate)
			inputObjectList[0] = realRate

			logger.warning("Warning: %s", "Output defined as Real, but Nominal rate was provided. \
				Real rate has been calculated from available inputs and will be used in subsequent calculations.")
			return inputObjectList

		elif not self.outputRealBool and self.dRateReal and self.inflationRate:
			nomRate = discounting.dRateNomCalc(self.dRateReal, self.inflationRate)
			inputObjectList[1] = nomRate

			logger.warning("Warning: %s", "Output defined as Nominal, but Real rate was provided. \
				Nominal rate has been calculated from available inputs and will be used in subsequent calculations.")
			return inputObjectList

		elif (self.outputRealBool and self.dRateReal and not self.dRateNom and not self.inflationRate) or \
			(not self.outputRealBool and self.dRateNom and not self.dRateReal and not self.inflationRate):
			logger.warning("Warning: %s", "Inflation rate is not calculable from given values. Calculations will proceed \
				unaffected however no inflation rate will be reported with output.")
		else:
			logger.error("Error: %s", "Error: Improper information given for discount rate. Calculation cannot proceed.")
			# Halts all calculations.
			nomRate = discounting.dRateNomCalc(self.dRateReal, self.inflationRate)
			inputObjectList[1] = nomRate
			
			return inputObjectList
