from typing import Any, Sequence

from API.serializers import CostType


def presentValue(v: CostType, d: CostType, t: CostType, e: CostType = 0) -> CostType:
    return v * ((1 + e) / (1 + d)) ** t


def createArray(studyPeriod: int, default: Any = 0):
    return [default] * (studyPeriod + 1)


class Bcn:
    def __init__(self, studyPeriod, **kwargs):
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
            self.recurVarValue = createArray(studyPeriod, default=self.recurVarValue)

        if not isinstance(self.quantVarValue, Sequence):
            self.quantVarValue = createArray(studyPeriod, default=self.quantVarValue)

    def __repr__(self) -> str:
        return f"BCN ID: {self.bcnID}"

    def discount(self, studyPeriod: int, rate: CostType) -> Sequence[CostType]:
        """
        Discounts this BCN to its present value.

        :param studyPeriod: The range that this BCN is over.
        :param rate:  The discount rate.
        :return: A list of discounted values over the study period.
        """
        result = createArray(studyPeriod)

        for i in range(self.initialOcc, self.recurEndDate):
            result[i] = presentValue(
                self.valuePerQ * (self.quant * self.quantVarValue[i - self.initialOcc]),
                rate,
                CostType(i),
                self.recurVarValue[i]
            )

        return result
