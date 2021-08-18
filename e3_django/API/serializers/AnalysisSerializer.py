from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField, IntegerField, DateField, DecimalField, ListField, CharField
from rest_framework.serializers import Serializer

from API.variables import MAX_DIGITS, DECIMAL_PLACES
from API.serializers.fields import ListMultipleChoiceField, BooleanOptionField
import logging

logger = logging.getLogger(__name__)

class AnalysisSerializer(Serializer):
    analysisType = ChoiceField(["LCCA", "BCA", "Cost-Loss", "Profit Maximization", "Other"], default="Default", required=False)
    projectType = ChoiceField(["Buildings", "Infrastructure", "Resilience", "Manufacturing Process", "Other"],
                              required=False)
    objToReport = ListMultipleChoiceField(
        ["FlowSummary", "MeasureSummary", "SensitivitySummary", "UncertaintySummary", "IRRSummary"],
        required=False
    )
    studyPeriod = IntegerField(min_value=0, required=False)
    baseDate = DateField(required=False)
    serviceDate = DateField(required=False)
    timestepVal = ChoiceField(["Year", "Quarter", "Month", "Day"], required=False)
    timestepComp = IntegerField(min_value=0, required=False)
    outputRealBool = BooleanOptionField({"Nominal", "0"}, {"Real", "1"}, required=False)
    interestRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    dRateReal = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    dRateNom = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    inflationRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    Marr = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    reinvestRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    incomeRateFed = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    incomeRateOther = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    location = ListField(child=CharField(), required=False)
    noAlt = IntegerField(min_value=0, required=True)
    baseAlt = IntegerField(min_value=0, required=True)
    

    def validate(self, data):
        # Ensure service date is after base date
        if data["serviceDate"] <= data["baseDate"]:
            raise ValidationError("Service Date must be after base date")

        # Ensure timestepComp is less than studyPeriod
        if data["timestepComp"] >= data["studyPeriod"]:
            raise ValidationError("timestepComp must be less than studyPeriod")

        # Depending on analysisType (LCCA, BCA, Cost-Loss, Profit Maximization), check all required inputs are included
            # Else, raise ValidationError

        return data

    def validateDiscountRate(self, data):
        inputObjectList = [data['dRateReal'], data['dRateNom'], data['inflationRate'], data['outputRealBool']]

        if not (data['outputRealBool'] and data['dRateReal'] and data['inflationRate'] and not data['dRateNom']) and not \
        (not data['outputRealBool'] and data['dRateNom'] and data['inflationRate'] and not data['dRateReal']):
            raise ValidationError("Check that all inputs are provided.")
        
        # aggregates all errors/warnings, rather than returning immediately.
        elif (data['outputRealBool'] and data['dRateReal'] and data['inflationRate'] and data['dRateNom']) or \
			(not data['outputRealBool'] and data['dRateNom'] and data['inflationRate'] and data['dRateReal']):
            inflRateCalc = discounting.inflationRateCalc(data['dRateNom'], data['RateReal'])
            if math.abs(inflRateCalc - data['inflationRate']) > 0.01: # if inflRateCalc is NOT within tolerance (start at 1%, adjust as needed)
                logger.warning("Warning: %s", "Note: The calculated inflation rate does not match the provided inflation rate.")
		
        elif data['outputRealBool'] and data['dRateNom'] and data['dRateReal']:
            # using dRateReal
            if not data['inflationRate']:
                inputObjectList[2] = discounting.inflationRate(data['dRateNom'], data['dRateReal'])
                logger.warning("Warning: %s", "Only the real rate will be used in calculations.")

        elif data['outputRealBool'] and data['dRateNom'] and data['dRateReal']:
			# using dRateNom
            if not self.inflationRate:
                inputObjectList[2] = discounting.inflationRate(data['dRateNom'], data['dRateReal'])
                logger.warning("Warning: %s", "Only the nominal rate will be used in calculations.")

        elif data['outputRealBool'] and data['dRateNom'] and data['inflationRate']:
            inputObjectList[0] = realRate = discounting.dRateRealCalc(data['dRateNom'], data['inflationRate'])
            logger.warning("Warning: %s", "Real rate was calculated from available inputs. It will be used in subsequent calculations.")

        elif not data['outputRealBool'] and data['dRateReal'] and data['inflationRate']:
            inputObjectList[1] = discounting.dRateNomCalc(data['dRateReal'], data['inflationRate'])
            logger.warning("Warning: %s", "Nominal rate was calculated from available inputs. It will be used in subsequent calculations.")

        elif (data['outputRealBool'] and data['dRateReal'] and not data['dRateNom'] and not data['inflationRate']) or \
			(not data['outputRealBool'] and data['dRateNom'] and not data['dRateReal'] and not data['inflationRate']):
            logger.warning("Warning: %s", "Inflation rate could not be calculated from given values.")
        else:
            logger.error("Error: %s", "Error: Improper discount rate provided. Calculation could not proceed.")
			# Halts all calculations.
            inputObjectList[1] = discounting.dRateNomCalc(self.dRateReal, self.inflationRate)
			
        return data

