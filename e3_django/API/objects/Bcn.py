from typing import Any, Sequence, Callable

from API.variables import CostType, FlowType


def present_value(v: CostType, d: CostType, t: CostType) -> CostType:
    """
    Converts the given value to a present value with the given discount and time values.

    :param v: The value to discount.
    :param d: The discount rate to apply.
    :param t: The amount of time to discount.
    :return: The value discounted to its present value.
    """
    return v * (1 / (1 + d)) ** t


def create_list(size: int, default: Any = 0):
    """
    Create an list of the given size plus one pre-populated with the given default parameter. Default is 0.

    :param size: The size of the list to create.
    :param default: The value to pre-populate the list with. Default is 0.
    :return: A list of the given size plus one pre-populated with the given default value.
    """
    return [CostType(default)] * (size + 1)


def discount_values(rate: CostType, values: list[CostType]):
    return list(map(lambda x: present_value(x[1], rate, CostType(x[0])), enumerate(values)))


class Bcn:
    """
    Represents a BCN object in the API input.
    """

    def __init__(self, studyPeriod, **kwargs):
        self.bcnID = kwargs.get("bcnID", None)
        self.altID = kwargs.get("altID", [])
        self.bcnType = kwargs.get("bcnType", None)
        self.bcnTag = kwargs.get("bcnTag", [])
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
            self.recurVarValue = create_list(studyPeriod, default=self.recurVarValue if self.recurVarValue else 0)
        if not isinstance(self.quantVarValue, Sequence):
            self.quantVarValue = create_list(studyPeriod, default=self.quantVarValue if self.quantVarValue else 0)
        if not isinstance(self.bcnTag, list):
            self.bcnTag = [self.bcnTag]

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

    def cash_flows(self, study_period: int, rate: CostType) -> FlowType:
        """
        Discounts this BCN to its present value and returns final and intermediate values.

        :param study_period: The range that this BCN is over.
        :param rate:  The discount rate.
        :return: A tuple of discounted values over the study period.
        """
        if not isinstance(rate, CostType):
            rate = CostType(rate)

        quantities = self.quantities(study_period)
        values = self.values(study_period, quantities)

        if self.rvBool:
            values = self.residual_value(study_period, values)

        discounted_values = discount_values(rate, values)

        return quantities, values, discounted_values

    def values(self, study_period: int, quantities: list[CostType]) -> list[CostType]:
        """
        Calculates the non-discounted values for over the study period from the given quantities.

        :param study_period: The study period the analysis is over.
        :param quantities: A list of quantities in the study period.
        :return: A list of non-discounted values in the correct position in a study period length array.
        """
        return self.period_calc(
            study_period,
            lambda i, _: quantities[i] * self.valuePerQ * ((1 + self.recurVarValue[i - self.initialOcc - 1]) ** i)
        )

    def quantities(self, study_period: int) -> list[CostType]:
        """
        Calculates the quantities over the study period.

        :param study_period: The study period the analysis is over.
        :return: A list of quantities at the correct position in a study period length array.
        """
        return self.period_calc(
            study_period,
            lambda i, previous: previous * (1 + self.quantVarValue[i - self.initialOcc - 1]),
            initial=self.quant
        )

    def period_calc(self, study_period: int, calculation: Callable, initial: CostType = None) -> list[CostType]:
        """
        Performs the specified calculation on an array from the initial occurrence to the recur end date. The
        calculation must be a function or lambda that accepts the current index and the previous value as parameters.
        For the first value, you can specify an initial value to pass to the calculation.

        :param study_period: The study period of the bcn.
        :param calculation: The function to run for every index in the BCN range.
        :param initial: The initial value to pass to the calculation for the first calculation.
        :return: A list of the study period with the values created by the calculation for the BCN range.
        """
        result = create_list(study_period)

        for i in range(self.initialOcc, self.recurEndDate + 1):
            result[i] = calculation(i, result[i - 1] if i > self.initialOcc else initial)

        return result

    def residual_value(self, study_period: int, values: Sequence[CostType]) -> list[CostType]:
        """
        Calculate the residual value of the bcn and place the resulting value in the give values array.
        
        :param study_period: The length of the study period.
        :param values: The list of values to place the result in to.
        :return: The list of values with the new residual value added.
        """
        result = list(values)

        if study_period >= self.bcnLife + self.initialOcc - 1:
            remaining_life = 0
        else:
            remaining_life = self.bcnLife - (study_period - self.initialOcc) - 1

        result[study_period] = CostType(-remaining_life / self.bcnLife) * values[self.initialOcc]

        return result
