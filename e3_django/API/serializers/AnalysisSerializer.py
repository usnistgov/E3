from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField, IntegerField, DateField, DecimalField, ListField, CharField
from rest_framework.serializers import Serializer

from API.objects.Analysis import calculate_inflation_rate, calculate_discount_rate_nominal, calculate_discount_rate_real
from API.variables import MAX_DIGITS, DECIMAL_PLACES, NUM_ERRORS_LIMIT
from API.serializers.fields import ListMultipleChoiceField, BooleanOptionField

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
    interestRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False, allow_null=True)
    dRateReal = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False, allow_null=True)
    dRateNom = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False, allow_null=True)
    inflationRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False, allow_null=True)
    Marr = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False, default=None)
    reinvestRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False, default=None)
    incomeRateFed = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False, allow_null=True)
    incomeRateOther = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False, allow_null=True)
    location = ListField(child=CharField(allow_blank=True), required=False)
    noAlt = IntegerField(min_value=0, required=True)
    baseAlt = IntegerField(min_value=0, required=True)

    def validate(self, data):
        errors = []

        # Ensure service date is after base date
        try:
            assert data["serviceDate"] >= data["baseDate"]:
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
                    "timestepComp must be less than studyPeriod"
                )
            )

        # Depending on analysisType (LCCA, BCA, Cost-Loss, Profit Maximization), check all required inputs are included
            # Else, raise ValidationError

        # Check if real discount rate boolean is True
        if data["outputRealBool"]:
            if not data["dRateReal"]:  # If dRateReal is NOT provided, try calculating it using dRateNom and inflationRate.
                if (data["dRateNom"] and data["inflationRate"]):
                    data["dRateReal"] = calculate_discount_rate_real(data["dRateNom"], data["inflationRate"])
                else:
                    errors.append(
                        ValidationError(
                            """Cannot calculate real discount rate from given inputs. Provide either:
                            (1) `real discount rate`, or
                            (2) `nominal discount rate` AND `inflation rate`.
                            """
                        )
                    )
        else:  # discount rate bool is False
            # If two of: dRateReal, dRateNom, inflationRate is provided, calculate the missing value:
            if data["dRateReal"] and data["inflationRate"]:
                data["dRateNom"] = calculate_discount_rate_nominal(data["inflationRate"], data["dRateReal"])

            elif data["dRateReal"] and data["dRateNom"]:
                data["inflationRate"] = calculate_inflation_rate(data["dRateNom"], data["dRateReal"])
                
            elif data["dRateNom"] and data["inflationRate"]:
                data["dRateReal"] = calculate_discount_rate_real(data["dRateNom"], data["inflationRate"])
            
            else: # If at least two of the above are not provided, raise Error.
                errors.append(
                    ValidationError(
                        """At least two of: inflationRate, dRateNom, dRateReal must be provided to calculate
                        nominal discount rate.
                        """
                    )
                )
                
        if errors:
            raise(Exception(errors[:NUM_ERRORS_LIMIT])) # Throws up to NUM_ERRORS_LIMIT number of errors.

        return data

