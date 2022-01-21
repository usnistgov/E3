from typing import Any, Sequence

from API.variables import CostType


def create_list(size: int, default: Any = 0):
    """
    Create an list of the given size plus one pre-populated with the given default parameter. Default is 0.

    :param size: The size of the list to create.
    :param default: The value to pre-populate the list with. Default is 0.
    :return: A list of the given size plus one pre-populated with the given default value.
    """
    return [CostType(default)] * (size + 1)


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

        if self.bcnLife is None:
            self.bcnLife = studyPeriod

    def __repr__(self) -> str:
        return f"BCN ID: {self.bcnID}"
