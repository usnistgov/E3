from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField, IntegerField, DateField, DecimalField, ListField, CharField
from rest_framework.serializers import Serializer

from API.objects.Analysis import calculate_inflation_rate, calculate_discount_rate_nominal, calculate_discount_rate_real
from API.variables import MAX_DIGITS, DECIMAL_PLACES
from API.serializers.fields import ListMultipleChoiceField, BooleanOptionField
import logging

logger = logging.getLogger(__name__)


REPORTABLE_OBJECTS = [
    "FlowSummary",
    "MeasureSummary",
    "OptionalSummary",
    "SensitivitySummary",
    "UncertaintySummary",
    "IRRSummary"
]

class AnalysisSerializer(Serializer):
    """
    Object serializer for analysis object.
    """

    analysisType = ChoiceField(["LCCA", "BCA", "Cost-Loss", "Profit Maximization", "Other"], default="Default", required=False)
    projectType = ChoiceField(["Buildings", "Infrastructure", "Resilience", "Manufacturing Process", "Other"],
                              required=False)
    objToReport = ListMultipleChoiceField(REPORTABLE_OBJECTS, required=False)
    studyPeriod = IntegerField(min_value=0, required=False)
    baseDate = DateField(required=False)
    serviceDate = DateField(required=False)
    timestepVal = ChoiceField(["Year", "Quarter", "Month", "Day"], required=False)
    timestepComp = IntegerField(min_value=0, required=False)
    outputRealBool = BooleanOptionField({"Nominal", "0"}, {"Real", "1"}, required=False)
    interestRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    dRateReal = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False, allow_null=True)
    dRateNom = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False, allow_null=True)
    inflationRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False, allow_null=True)
    Marr = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    reinvestRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    incomeRateFed = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    incomeRateOther = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    location = ListField(child=CharField(allow_blank=True), required=False)
    noAlt = IntegerField(min_value=0, required=True)
    baseAlt = IntegerField(min_value=0, required=True)

    def validate(self, data):
        # Ensure service date is after base date
        if data["serviceDate"] < data["baseDate"]:
            raise ValidationError("Service Date must be after base date")

        # Ensure timestepComp is less than studyPeriod
        if data["timestepComp"] >= data["studyPeriod"]:
            raise ValidationError("timestepComp must be less than studyPeriod")

        # Depending on analysisType (LCCA, BCA, Cost-Loss, Profit Maximization), check all required inputs are included
            # Else, raise ValidationError

        # Ensure at least two of (inflation rate, real discount rate, nominal discount rate) are provided for calculation
        if not data["inflationRate"] and not data["dRateNom"] and not data["dRateReal"]:
            raise ValidationError("Err: interest rate, real discount rate, and nominal discount rate are all missing.")

        elif data["inflationRate"] and not data["dRateNom"] and not data["dRateReal"]:
            raise ValidationError("Err: real discount rate and nominal discount rate are both missing.")

        elif data["dRateNom"] and not data["dRateReal"] and not data["inflationRate"]:
            raise ValidationError("Err: inflation rate and real discount rate are both missing.")

        elif data["dRateReal"] and not data["inflationRate"] and not data["dRateNom"]:
            raise ValidationError("Err: inflation rate and nominal discount rate are both missing.")


        if data["outputRealBool"] and not data["dRateReal"]:
            if not data["dRateNom"] or not data["inflationRate"]:
                raise ValidationError("Cannot calculate real discount rate.")
            data["dRateReal"] = calculate_discount_rate_real(data["dRateNom"], data["inflationRate"])

        elif not data["outputRealBool"] and not data["dRateNom"]:
            if not data["dRateReal"] or not data["inflationRate"]:
                raise ValidationError("Cannot calculate nominal discount rate.")
            data["dRateNom"] = calculate_discount_rate_nominal(data["dRateReal"], data["inflationRate"])

        return data

