import logging
from typing import Any, Sequence, Tuple, Callable

from API.serializers import CostType


def presentValue(v: CostType, d: CostType, t: CostType) -> CostType:
    return v * (1 / (1 + d)) ** t


def createArray(studyPeriod: int, default: Any = 0):
    return [CostType(default)] * (studyPeriod + 1)


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
        self.valuePerQ = kwargs.get("valuePerQ", 0)
        self.quant = kwargs.get("quant", None)
        self.quantVarRate = kwargs.get("quantVarRate", None)
        self.quantVarValue = kwargs.get("quantVarValue", CostType(0))
        self.quantUnit = kwargs.get("quantUnit", None)

        # Inflate single values to arrays to make later computations easier
        if not isinstance(self.recurVarValue, Sequence):
            self.recurVarValue = createArray(studyPeriod, default=self.recurVarValue if self.recurVarValue else 0)
        if not isinstance(self.quantVarValue, Sequence):
            self.quantVarValue = createArray(studyPeriod, default=self.quantVarValue if self.quantVarValue else 0)

        # If end date does not exist, set to studyPeriod if recur is true, else set to initial occurrence for single
        # value.
        if self.recurEndDate is None:
            self.recurEndDate = studyPeriod if self.recurBool else self.initialOcc

        # Ensure values are correct type for computation
        if not all([isinstance(value, CostType) for value in self.recurVarValue]):
            self.recurVarValue = [CostType(value) for value in self.recurVarValue]
        if not all([isinstance(value, CostType) for value in self.quantVarValue]):
            self.quantVarValue = [CostType(value) for value in self.quantVarValue]
        if not isinstance(self.valuePerQ, CostType):
            self.valuePerQ = CostType(self.valuePerQ)

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
        if not isinstance(rate, CostType):
            rate = CostType(rate)

        quantities = self.quantities(studyPeriod)
        values = self.values(studyPeriod, quantities)

        if self.rvBool:
            values = self.residualValue(studyPeriod, values)

        discountedValues = discountValues(rate, values)

        return quantities, values, discountedValues

    def values(self, studyPeriod: int, quantities: Sequence[CostType]) -> Sequence[CostType]:
        """
        Calculates the non-discounted values for over the study period from the given quantities.

        :param studyPeriod: The study period the analysis is over.
        :param quantities: A list of quantities in the study period.
        :return: A list of non-discounted values in the correct position in a study period length array.
        """
        return self.periodCalc(
            studyPeriod,
            lambda i, _: quantities[i] * self.valuePerQ * ((1 + self.recurVarValue[i - self.initialOcc - 1]) ** i)
        )

    def quantities(self, studyPeriod: int) -> Sequence[CostType]:
        """
        Calculates the quantities over the study period.

        :param studyPeriod: The study period the analysis is over.
        :return: A list of quantities at the correct position in a study period length array.
        """
        return self.periodCalc(
            studyPeriod,
            lambda i, previous: previous * (1 + self.quantVarValue[i - self.initialOcc - 1]),
            initial=self.quant
        )

    def periodCalc(self, studyPeriod: int, calculation: Callable, initial: CostType = None) -> Sequence[CostType]:
        result = createArray(studyPeriod)

        for i in range(self.initialOcc, self.recurEndDate + 1):
            result[i] = calculation(i, result[i - 1] if i > self.initialOcc else initial)

        return result

    def residualValue(self, studyPeriod: int, values: Sequence[CostType]) -> Sequence[CostType]:
        # TODO fix this to work in edge cases
        result = list(values)

        result[studyPeriod] = CostType((studyPeriod - self.bcnLife) / self.bcnLife) * values[self.initialOcc]

        return result
