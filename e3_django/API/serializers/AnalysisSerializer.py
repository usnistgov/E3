from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField, IntegerField, DateField, DecimalField, ListField, CharField
from rest_framework.serializers import Serializer

from API.objects.Analysis import calculate_inflation_rate, calculate_discount_rate_nominal, calculate_discount_rate_real
from API.variables import MAX_DIGITS, DECIMAL_PLACES, NUM_ERRORS_LIMIT
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
    projectType = ChoiceField(["Buildings", "Infrastructure", "Resilience", "Manufacturing Process", "Other"], required=False)
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
        errors = []

        # Ensure service date is after base date
        try: 
            assert data["serviceDate"] >= data["baseDate"]
        except: 
            errors.append(
                ValidationError(
                    "Service Date must be after base date"
                )
            )

        # Ensure timestepComp is less than studyPeriod
        try:
            assert data["timestepComp"] < data["studyPeriod"]:
        except:
            errors.append(
                ValidationError(
                    "TimestepComp must be less than studyPeriod"
                )
            )

        # Depending on analysisType (LCCA, BCA, Cost-Loss, Profit Maximization), check all required inputs are included
            # Else, raise ValidationError

        # Ensure at least two of (inflation rate, real discount rate, nominal discount rate) are provided 
        vars_required_for_calc = [data["inflationRate"], data["dRateNom"], data["dRateReal"]]

        if all(vars_required_for_calc): 
            # Valid for calculation, since all three variables exist
            pass
        else:
            try:
                assert sum(1 for v in vars_required_for_calc if v) >= 2
            except:
                errors.append(
                    ValidationError(
                        """At least two values out of 'interest rate', 'real discount rate', or 'nominal discount rate' 
                        must be provided to make calculations. 

                        For instance, provide either:
                        (1) `interest rate` AND `real discount rate`, 
                        (2) `interest rate` AND `nominal discount rate`, 
                        (3) `real discount rate` AND `nominal discount rate`, 
                        or (4) all three.
                        """
                    )
                )

        # Ensure required variables are provided, depending on `outputRealBool' (real/nominal discount rate)
        if data["outputRealBool"] and not data["dRateReal"]: # Real discount rate selected
            try:
                data["dRateReal"] = calculate_discount_rate_real(data["dRateNom"], data["inflationRate"])
            except:
                errors.append(
                    ValidationError(
                        """In order to calculate discount rate as a `real` value, both nominal discount rate and inflation rate 
                        must be provided.
                        """
                    )
                )
        elif not data["outputRealBool"] and not data["dRateNom"]: # Nominal discount rate selected
            try:
                data["dRateNom"] = calculate_discount_rate_nominal(data["dRateReal"], data["inflationRate"])
            except:
                errors.append(
                    ValidationError(
                        """In order to calculate discount rate as a `nominal` value, both nominal discount rate and inflation rate
                        must be provided.
                        """
                    )
                )

        if errors:
            raise(Exception(errors[:NUM_ERRORS_LIMIT]) # Throws up to NUM_ERRORS_LIMIT number of errors.

        return data

