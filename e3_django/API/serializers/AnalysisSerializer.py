from rest_framework.exceptions import ValidationError
from rest_framework.fields import ChoiceField, IntegerField, DateField, DecimalField, ListField, CharField
from rest_framework.serializers import Serializer

from API.serializers import MAX_DIGITS, DECIMAL_PLACES
from API.serializers.fields import ListMultipleChoiceField, BooleanOptionField


class AnalysisSerializer(Serializer):
    analysisType = ChoiceField(["LCC", "BCA", "Cost-Loss", "Profit Maximization", "Other"], required=True)
    projectType = ChoiceField(["Buildings", "Infrastructure", "Resilience", "Manufacturing Process", "Other"],
                              required=False)
    objToReport = ListMultipleChoiceField(
        ["FlowSummary", "MeasureSummary", "SensitivitySummary", "UncertaintySummary", "IRRSummary"],
        required=True
    )
    studyPeriod = IntegerField(min_value=0, required=True)
    baseDate = DateField(required=True)
    serviceDate = DateField(required=False)
    timestepVal = ChoiceField(["Year", "Quarter", "Month", "Day"], required=True)
    timestepComp = IntegerField(min_value=0, required=True)
    outputRealBool = BooleanOptionField({"Nominal", "0"}, {"Real", "1"}, required=False)
    interestRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    dRateReal = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    dRateNom = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    inflationRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    Marr = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    reinvestRate = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    incomeRateFed = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    incomeRateOther = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    noAlt = IntegerField(min_value=0, required=True)
    baseAlt = IntegerField(min_value=0, required=True)
    location = ListField(child=CharField(), required=False)

    def validate(self, data):
        # Ensure service date is after base date
        if data["serviceDate"] < data["baseDate"]:
            raise ValidationError("Service Date must be after base date")

        # Ensure timestepComp is less than studyPeriod
        if data["timestepComp"] > data["studyPeriod"]:
            raise ValidationError("timestepComp must be less than studyPeriod")

        return data
