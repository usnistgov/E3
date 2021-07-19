from typing import Any, Sequence, Tuple

from API.serializers import CostType


def presentValue(v: CostType, d: CostType, t: CostType) -> CostType:
    return v * (1 / (1 + d)) ** t


def createArray(studyPeriod: int, default: Any = CostType(0)):
    return [default] * (studyPeriod + 1)


def discountValues(rate: CostType, values: Sequence[CostType]):
    return list(map(lambda x: presentValue(x[1], rate, CostType(x[0])), enumerate(values)))


class Bcn:
    def __init__(self, studyPeriod, **kwargs):
        self.bcnID = kwargs.get("bcnID", None)
        self.altID = kwargs.get("altID", None)
        self.bcnType = kwargs.get("bcnType", None)
        self.bcnSubType = kwargs.get("bcnSubType", None)
        self.bcnName = kwargs.get("bcnName", None)
        self.initialOcc = kwargs.get("initialOcc", 0)
        self.bcnLife = kwargs.get("bcnLife", None)
        self.bcnRealBool = kwargs.get("bcnRealBool", None)
        self.bcnInvestBool = kwargs.get("bcnInvestBool", False)
        self.rvBool = kwargs.get("rvBool", None)
        self.recurBool = kwargs.get("recurBool", None)
        self.recurInterval = kwargs.get("recurInterval", None)
        self.recurVarRate = kwargs.get("recurVarRate", None)
        self.recurVarValue = kwargs.get("recurVarValue", CostType(0))
        self.recurEndDate = kwargs.get("recurEndDate", self.initialOcc)
        self.valuePerQ = kwargs.get("valuePerQ", None)
        self.quant = kwargs.get("quant", None)
        self.quantVarRate = kwargs.get("quantVarRate", None)
        self.quantVarValue = kwargs.get("quantVarValue", CostType(0))
        self.quantUnit = kwargs.get("quantUnit", None)

        if not isinstance(self.recurVarValue, Sequence):
            self.recurVarValue = createArray(studyPeriod, default=self.recurVarValue if self.recurVarValue else CostType(0))

        if not isinstance(self.quantVarValue, Sequence):
            self.quantVarValue = createArray(studyPeriod, default=self.quantVarValue if self.quantVarValue else CostType(0))

        if self.recurEndDate is None:
            self.recurEndDate = studyPeriod if self.recurBool else self.initialOcc

    def __repr__(self) -> str:
        return f"BCN ID: {self.bcnID}"

    def cashFlows(self, studyPeriod: int, rate: CostType) \
            -> Tuple[Sequence[CostType], Sequence[CostType], Sequence[CostType]]:
        """
        Discounts this BCN to its present value.

        :param studyPeriod: The range that this BCN is over.
        :param rate:  The discount rate.
        :return: A list of discounted values over the study period.
        """
        quantities = self.quantities(studyPeriod)
        values = self.values(studyPeriod, quantities)

        if self.rvBool:
            values = self.residualValue(studyPeriod, values)

        discountedValues = discountValues(rate, values)

        return quantities, values, discountedValues

    def values(self, studyPeriod, quantities):
        return self.periodCalc(
            studyPeriod,
            lambda i, _: quantities[i] * self.valuePerQ * ((CostType(1) + self.recurVarValue[i - self.initialOcc - 1]) ** i)
        )

    def quantities(self, studyPeriod):
        return self.periodCalc(
            studyPeriod,
            lambda i, previous: previous * (1 + self.quantVarValue[i - self.initialOcc - 1]),
            initial=self.quant
        )

    def periodCalc(self, studyPeriod, calculation, initial=None):
        result = createArray(studyPeriod)

        for i in range(self.initialOcc, self.recurEndDate + 1):
            result[i] = calculation(i, result[i - 1] if i > self.initialOcc else initial)

        return result

    def residualValue(self, studyPeriod, values):
        # TODO fix this to work in edge cases
        result = list(values)

        result[studyPeriod] = CostType((studyPeriod - self.bcnLife) / self.bcnLife) * values[self.initialOcc]

        return result
