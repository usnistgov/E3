from rest_framework.serializers import *
from drf_compound_fields.fields import ListOrItemField

MAX_DIGITS = 20
DECIMAL_PLACES = 5


class BooleanOptionField(Field):
    default_error_messages = {
        'none': 'Original value cannot be None.',
        'invalid': 'Input must be a valid option.'
    }

    def __init__(self, true_values, false_values, required=False):
        super().__init__(required=required)

        self.original_value = None

        true_values.add(True)
        self.true_values = true_values

        false_values.add(False)
        self.false_values = false_values

    def to_representation(self, value):
        if self.original_value is None:
            self.fail("none")

        return f"{self.original_value}"

    def to_internal_value(self, data):
        self.original_value = data

        if data in self.true_values:
            return True
        elif data in self.false_values:
            return False
        else:
            self.fail("invalid")


class AnalysisSerializer(Serializer):
    analysisType = ChoiceField(["LCC", "BCA", "Cost-Loss", "Profit Maximization", "Other"], required=True)
    projectType = ChoiceField(["Buildings", "Infrastructure", "Resilience", "Manufacturing Process", "Other"], required=False)
    objToReport = MultipleChoiceField(
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


class AlternativeSerializer(Serializer):
    altID = IntegerField(min_value=0, required=True)
    altName = CharField(required=False)
    altBCNList = ListField(child=IntegerField(), required=False)
    baselineBool = BooleanField(required=False)


class BCNSerializer(Serializer):
    bcnID = IntegerField(min_value=0, required=True)
    altID = ListField(child=IntegerField(min_value=0, required=False), required=True)
    bcnType = ChoiceField(["Benefit", "Cost", "NonMonetary", "0", "1", "2"], required=False)
    bcnSubType = ChoiceField(["Direct", "Indirect", "Externality", "0", "1", "2"], required=False)
    bcnName = CharField(required=False)
    bcnTag = CharField(required=False)
    initialOcc = IntegerField(min_value=0, required=False)
    bcnRealBool = BooleanOptionField({"Nominal", "0"}, {"Real", "1"}, required=False)
    bcnInvestBool = BooleanField(required=False)
    bcnLife = IntegerField(min_value=0, required=False)
    rvBool = BooleanField(required=False)
    recurBool = BooleanField(required=False)
    recurInterval = IntegerField(min_value=0, required=False)
    recurVarRate = ChoiceField(["Percent Delta Timestep X-1"], required=False)
    recurVarValue = ListOrItemField(DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), required=False)
    recurEndDate = IntegerField(min_value=0, required=False)
    ValuePerQ = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    quant = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    quatVarRate = ChoiceField(["Percent Delta Timestep X-1"], required=False)
    quantVarValue = ListOrItemField(DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), required=False)
    quantUnit = CharField(required=False)


class SensitivitySerializer(Serializer):
    globalVarBool = BooleanField(required=True)
    altID = IntegerField(required=False) # TODO represent required property
    bcnID = IntegerField(required=False) # TODO represent required property
    varName = ChoiceField([
        "initialOcc", "bcnLife", "recurValue", "recurEndDate", "valuePerQ", "quant", 'quantValue'],
        required=True
    )
    diffType = ChoiceField(["Percent", "Gross"], required=True)
    diffValue = DecimalField(max_digits=7, decimal_places=2, required=True)


class ScenarioSerializer(Serializer):
    pass


class InputSerializer(Serializer):
    analysisObject = AnalysisSerializer(required=False)
    alternativeObjects = ListField(child=AlternativeSerializer(), required=False)
    bcnObjects = ListField(child=BCNSerializer(), required=False)
    sensitivityObject = SensitivitySerializer(required=False)
    scenarioObject = ScenarioSerializer(required=False)
