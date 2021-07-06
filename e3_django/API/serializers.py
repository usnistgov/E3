from __future__ import annotations

import logging
from decimal import Decimal
from typing import Sequence, Any

from drf_compound_fields.fields import ListOrItemField
from rest_framework.serializers import *

from API.fields import ListMultipleChoiceField, BooleanOptionField

logger = logging.getLogger(__name__)

MAX_DIGITS = 20
DECIMAL_PLACES = 5

CostType = Decimal


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


class AlternativeSerializer(Serializer):
    altID = IntegerField(min_value=0, required=True)
    altName = CharField(required=False)
    altBCNList = ListField(child=IntegerField(), required=False)
    baselineBool = BooleanField(required=False)


class Alternative:
    def __init__(self, *args, **kwargs):
        for key, value in args[0].items():
            logger.info(f"Key: {key}, Value: {value}")
            setattr(self, key, value)


class BCNSerializer(Serializer):
    bcnID = IntegerField(min_value=0, required=True)
    altID = ListField(child=IntegerField(min_value=0, required=False), required=False)
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
    valuePerQ = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    quant = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    quatVarRate = ChoiceField(["Percent Delta Timestep X-1"], required=False)
    quantVarValue = ListOrItemField(DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), required=False)
    quantUnit = CharField(required=False)


class SensitivitySerializer(Serializer):
    globalVarBool = BooleanField(required=True)
    altID = IntegerField(required=False)  # TODO represent required property
    bcnID = IntegerField(required=False)  # TODO represent required property
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


class CashFlow:
    altID = 0
    totCostDisc = []
    totCostsDiscInv = []
    totCostsNonDiscInv = []
    totBenefitsDisc = []
    totCostsDirDisc = []
    totCostsIndDisc = []
    totCostsExtDisc = []
    totBenefitsDirDisc = []
    totBenefitsIndDisc = []
    totBenefitsExtDisc = []

    def __init__(
            self,
            altID=0,
            totCostDisc=[],
            totCostsDiscInv=[],
            totCostsNonDiscInv=[],
            totBenefitsDisc=[],
            totCostsDirDisc=[],
            totCostsIndDisc=[],
            totCostsExtDisc=[],
            totBenefitsDirDisc=[],
            totBenefitsIndDisc=[],
            totBenefitsExtDisc=[]
    ):
        self.altID = altID
        self.totCostDisc = totCostDisc
        self.totCostsDiscInv = totCostsDiscInv
        self.totCostsDiscInv = totCostsDiscInv
        self.totCostsNonDiscInv = totCostsNonDiscInv
        self.totBenefitsDisc = totBenefitsDisc
        self.totCostsDirDisc = totCostsDirDisc
        self.totCostsIndDisc = totCostsIndDisc
        self.totCostsExtDisc = totCostsExtDisc
        self.totBenefitsDirDisc = totBenefitsDirDisc
        self.totoBenefitsIndDisc = totBenefitsIndDisc
        self.totBenefitsExtDisc = totBenefitsExtDisc


class CashFlowSerializer(Serializer):
    altID = IntegerField(required=True)
    totCostDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), required=False)
    totCostsDiscInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totCostsNonDiscInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totBenefitsDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totCostsDirDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totCostsIndDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totCostsExtDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totBenefitsDirDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totBenefitsIndDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totBenefitsExtDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)


class Output:
    def __init__(self, reqCashFlowObjects):
        self.reqCashFlowObjects = reqCashFlowObjects


class OutputSerializer(Serializer):
    reqCashFlowObjects = CashFlowSerializer()


def presentValue(v: CostType, d: CostType, t: CostType, e: CostType = 0) -> CostType:
    return v * ((1 + e) / (1 + d)) ** t


class BCN:
    def __init__(self, studyPeriod, **kwargs):
        self.studyPeriod = studyPeriod

        self.bcnID = kwargs.get("bcnID", None)
        self.altID = kwargs.get("altID", None)
        self.bcnType = kwargs.get("bcnType", None)
        self.bcnSubType = kwargs.get("bcnSubType", None)
        self.bcnName = kwargs.get("bcnName", None)
        self.initialOcc = kwargs.get("initialOcc", 0)
        self.bcnRealBool = kwargs.get("bcnRealBool", None)
        self.bcnInvestBool = kwargs.get("bcnInvestBool", None)
        self.rvBool = kwargs.get("rvBool", None)
        self.recurBool = kwargs.get("recurBool", None)
        self.recurInterval = kwargs.get("recurInterval", None)
        self.recurVarRate = kwargs.get("recurVarRate", None)
        self.recurVarValue = kwargs.get("recurVarValue", 0)
        self.recurEndDate = kwargs.get("recurEndDate", self.initialOcc + 1)
        self.valuePerQ = kwargs.get("valuePerQ", None)
        self.quant = kwargs.get("quant", None)
        self.quantVarRate = kwargs.get("quantVarRate", None)
        self.quantVarValue = kwargs.get("quantVarValue", 1)
        self.quantUnit = kwargs.get("quantUnit", None)

        if not isinstance(self.recurVarValue, Sequence):
            self.recurVarValue = self.createArray(self.recurVarValue)

        if not isinstance(self.quantVarValue, Sequence):
            self.quantVarValue = self.createArray(self.quantVarValue)

    def __repr__(self) -> str:
        return f"BCN ID: {self.bcnID}"

    def discount(self, rate: CostType) -> Sequence[CostType]:
        """
        Discounts this BCN to its present value.

        :param rate:  The discount rate.
        :return: A list of discounted values over the study period.
        """
        result = self.createArray()

        for i in range(self.initialOcc, self.recurEndDate):
            result[i] = presentValue(
                self.valuePerQ * (self.quant * self.quantVarValue[i - self.initialOcc]),
                rate,
                CostType(i),
                self.recurVarValue[i]
            )

        return result

    def createArray(self, default: Any = 0):
        return [default] * (self.studyPeriod + 1)
