
from API.objects import Bcn

class Sensitivity:
    """
    Represents the sensitivity object of the API input.
    """

    def __init__(
        self,
        globalVarBool,
        altID,
        bcnID,
        varName,
        diffType,
        diffValue
    ):
        # Boolean indicating global variable
        self.globalVarBool = globalVarBool

        # List of alternative IDs
        self.altID = altID

        # BCN ID
        self.bcnID = bcnID

        # Variable to be changed
        self.varName = varName

        # Type of change to be made
        self.diffType = diffType

        # Value to be changed by
        self.diffValue = diffValue

        
        # Find BCN and variable defined in Sensitivity Object

        # Store original value

        # Update appropriate value in BCN object

        # Rerun analysis

        # Store output

        # Revert BCN Values 