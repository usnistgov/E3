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

        # Check if real discount rate boolean is True
        if data["outputRealBool"]:
            if data["dRateReal"]: 
                pass
            else: 
                if (data["dRateNom"] and data["inflationRate"]):
                    data["dRateReal"] = calculate_discount_rate_real(data["dRateNom"], data["inflationRate"])
                else:
                    raise ValidationError(
                        """Cannot calculate real discount rate from given inputs. Provide either:
                        (1) `real discount rate`, or
                        (2) `nominal discount rate` AND `inflation rate`.
                        """
                    )
        else:  # discount rate bool is False
            if data["dRateReal"] and data["inflationRate"]:
                data["dRateNom"] = calculate_discount_rate_nominal(data["inflationRate"], data["dRateReal"])
            elif data["dRateReal"] and data["dRateNom"]:
                data["inflationRate"] = calculate_inflation_rate(data["dRateNom"], data["dRateReal"])
            elif data["dRateNom"] and data["inflationRate"]:
                data["dRateReal"] = calculate_discount_rate_real(data["dRateNom"], data["inflationRate"])
            else:
                raise ValidationError("At least two of: inflationRate, dRateNom, dRateReal must be provided.")

        return data

