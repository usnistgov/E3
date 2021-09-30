import math
from typing import Any, Sequence, Generator

from API.variables import CostType, FlowType, VAR_RATE_OPTIONS


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
    """
    Discounts the given list of values to their present values with the given rate.

    :param rate: The discount rate.
    :param values: The list of values to discount.
    :return: A list of discounted values.
    """
    return list(map(lambda x: present_value(x[1], rate, CostType(x[0])), enumerate(values)))


class Bcn:
    """
    Represents a BCN object in the API input.
    """

    def __init__(self, studyPeriod, **kwargs):
        # BCN ID
        self.bcnID = kwargs.get("bcnID", None)

        # List of alternative IDs this BCN is a part of
        self.altID = kwargs.get("altID", [])

        # Type of this BCN
        self.bcnType = kwargs.get("bcnType", None)

        # Tag list for this BCN that determine which optional cash flows it is a part of
        self.bcnTag = kwargs.get("bcnTag", [])

        # Subtype of this BCN
        self.bcnSubType = kwargs.get("bcnSubType", None)

        # Name of this BCN
        self.bcnName = kwargs.get("bcnName", None)

        # The timestep where this BCN begins.
        self.initialOcc = kwargs.get("initialOcc", 0)

        # The number of timesteps before the BCN needs to be replaced.
        self.bcnLife = kwargs.get("bcnLife", None)

        # If true then value will be discounted, otherwise no discounting is done.
        self.bcnRealBool = kwargs.get("bcnRealBool", None)

        # BCN invest boolean
        self.bcnInvestBool = kwargs.get("bcnInvestBool", False)

        # Residual value boolean
        self.rvBool = kwargs.get("rvBool", None)

        # Only include residual value in cash flow and ignore all other values
        self.rvOnly = kwargs.get("rvOnly", False)

        # Recurrence boolean, determines whether this BCN is interpreted as a single value or a series of values.
        self.recurBool = kwargs.get("recurBool", None)

        # Number of timesteps between each recurrence step.
        self.recurInterval = kwargs.get("recurInterval", 1)

        # Type of recurrence variability.
        self.recurVarRate = kwargs.get("recurVarRate", None)

        # A single or list of values that define how the recurrence changes over timesteps.
        self.recurVarValue = kwargs.get("recurVarValue", CostType(0))

        # The timestep where the recurrence ends.
        self.recurEndDate = kwargs.get("recurEndDate", self.initialOcc)

        # The value of each quantity of this BCN.
        self.valuePerQ = kwargs.get("valuePerQ", 0)

        # The quantity of this BCN.
        self.quant = kwargs.get("quant", None)

        # Type of quantity variability.
        self.quantVarRate = kwargs.get("quantVarRate", None)

        # A single or list of values that define how the quantity changes over timesteps.
        self.quantVarValue = kwargs.get("quantVarValue", CostType(0))

        # Units of the quantity.
        self.quantUnit = kwargs.get("quantUnit", None)

        self.is_single_recur_value = isinstance(self.recurVarValue, CostType)
        self.is_recur_end_date_none = self.recurEndDate is None

        # Inflate single values to arrays to make later computations easier
        if not isinstance(self.recurVarValue, Sequence):
            self.recurVarValue = create_list(studyPeriod, default=self.recurVarValue if self.recurVarValue else 0)
        if not isinstance(self.quantVarValue, Sequence):
            self.quantVarValue = ([CostType("0")] * (self.initialOcc if self.initialOcc > 0 else 0)) + \
                                 create_list(studyPeriod - self.initialOcc,
                                             default=self.quantVarValue if self.quantVarValue else 0)
        if not isinstance(self.bcnTag, list):
            self.bcnTag = [self.bcnTag]

        # If end date does not exist, set to studyPeriod if recur is true, else set to initial occurrence for single
        # value.
        if self.recurEndDate is None:
            self.recurEndDate = studyPeriod if self.recurBool else self.initialOcc
        if self.recurInterval is None:
            self.recurInterval = 1

        # Ensure values are correct type for computation
        if not all([isinstance(value, CostType) for value in self.recurVarValue]):
            self.recurVarValue = [CostType(value) for value in self.recurVarValue]
        if not all([isinstance(value, CostType) for value in self.quantVarValue]):
            self.quantVarValue = [CostType(value) for value in self.quantVarValue]
        if not isinstance(self.valuePerQ, CostType):
            self.valuePerQ = CostType(self.valuePerQ if self.valuePerQ else 0)

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

        quantities = list(self.quantities(study_period))
        values = list(self.values(study_period, quantities))

        if self.rvBool:
            values = self.residual_value(study_period, values)

        discounted_values = discount_values(rate, values)

        return quantities, values, discounted_values

    def values(self, study_period: int, quantities: list[CostType]) -> Generator[CostType, None, None]:
        """
        Calculates the non-discounted values for over the study period from the given quantities.

        :param study_period: The study period the analysis is over.
        :param quantities: The list of quantities.
        :return: A list of non-discounted values in the correct position in a study period length array.
        """
        recur_var_value = self.get_recur_generator()
        return self.generator_base(
            study_period,
            lambda i: quantities[i] * self.valuePerQ * next(recur_var_value)
        )

    def get_recur_generator(self) -> Generator[CostType, None, None]:
        if self.is_single_recur_value:
            return self.single_value()

        if self.recurVarRate == VAR_RATE_OPTIONS[1]:
            return self.year_by_year(self.recurVarValue)

        return self.var_value(self.recurVarValue)

    def year_by_year(self, var_value_list) -> Generator[CostType, None, None]:
        """
        A generator which calculates var values year by year.

        :return: A generator returning the next var value.
        """
        for i in range(self.initialOcc, self.recurEndDate + 1):
            yield var_value_list[i]

    def single_value(self) -> Generator[CostType, None, None]:
        """
        A generator which calculates the var values for this BCN if they are not compounding.

        :return: A generator returning the next var value.
        """
        for i in range(0, self.recurEndDate + 1):
            if i >= self.initialOcc and (i - self.initialOcc) % self.recurInterval == 0:
                yield (1 + self.recurVarValue[i]) ** i

    def var_value(self, var_value_list) -> Generator[CostType, None, None]:
        """
        A generator which calculates the the var values for this BCN if they should be compounding.

        :return: A generator returning the next var value.
        """
        result = 1

        for i in range(0, self.recurEndDate + 1):
            if result == 0 and var_value_list[i] != 0:
                result = 1

            result = result * (1 + var_value_list[i])

            if i >= self.initialOcc and (i - self.initialOcc) % self.recurInterval == 0:
                yield result

    def quantities(self, study_period: int) -> Generator[CostType, None, None]:
        """
        Calculates the quantities over the study period.

        :param study_period: The study period the analysis is over.
        :return: A list of quantities at the correct position in a study period length array.
        """
        quantity_var_value = self.year_by_year(self.quantVarValue) if self.quantVarRate == VAR_RATE_OPTIONS[1] \
            else self.var_value(self.quantVarValue)
        return self.generator_base(study_period, lambda _: self.quant * next(quantity_var_value))

    def generator_base(self, study_period, calculation) -> Generator[CostType, None, None]:
        """
        Creates a generator which performs the given calculation in the correct time slots or else returns 0.

        :param study_period: The length of the study period, the generator will produce a list of this value plus one.
        :param calculation: A lambda which takes the current index and returns a CostType.
        :return: A generator which returns CostType objects.
        """
        for i in range(0, study_period + 1):
            if i < self.initialOcc or (i - self.initialOcc) % self.recurInterval or i > self.recurEndDate:
                yield CostType("0")
            else:
                yield calculation(i)

    def residual_value(self, study_period: int, values: Sequence[CostType]) -> list[CostType]:
        """
        Calculate the residual value of the bcn and place the resulting value in the give values array.
        
        :param study_period: The length of the study period.
        :param values: The list of values to place the result in to.
        :return: The list of values with the new residual value added.
        """
        result = [CostType(0)] * len(values) if self.rvOnly else list(values)
        remaining_life = self.remaining_life(study_period)

        print(f"---BCN: {self.bcnID}")
        print(f"Remaining Life: {remaining_life}, BCN Life: {self.bcnLife}, value: {values[self.initialOcc]}")

        result[study_period] += CostType(-remaining_life / self.bcnLife) * values[self.initialOcc]

        print(f"Residual Value: {result}")

        return result

    def remaining_life(self, study_period: int):
        """
        Calculate the remaining life of this bcn. This can change depending on if it is recurring, the properties
        of the recursion, or if it is a single cost.
        
        :param study_period: The length of the study period.
        :return: The remaining life of the bcn.
        """

        def last_interval():
            return math.floor((study_period - self.initialOcc) / self.recurInterval) * self.recurInterval \
                   + self.initialOcc

        def end_date_within_period():
            return not self.is_recur_end_date_none and self.recurEndDate <= study_period

        def lifetime_within_period():
            if self.recurBool and self.is_recur_end_date_none:
                return False

            return study_period >= self.bcnLife + last_interval() - 1

        if end_date_within_period() or lifetime_within_period():
            return 0
        elif self.recurBool:
            return self.bcnLife - (study_period - self.initialOcc - last_interval()) - 1
        else:
            return self.bcnLife - (study_period - self.initialOcc)
