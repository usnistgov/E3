
from API.objects import Bcn
import logging

from e3_django.API.serializers.InputSerializer import InputSerializer

logger = logging.getLogger(__name__)

class Sensitivity:
    """
    Represents the sensitivity object of the API input.
    """

    def __init__(
        self,
        globalVarBool,
        altID,
        bcnID,
        bcnObj,
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
        
        # BCN Object corresponding to BCN ID
        self.bcnObj = bcnObj

        # Variable to be changed
        self.varName = varName

        # Type of change to be made
        self.diffType = diffType

        # Value to be changed by
        self.diffValue = diffValue

    
    def calculateOutput(self):
        # Store original values
        original_val = self.bcnObj

        # E.g. cost_function(a,b,c) = a**2 + math.sqrt(b) - c//2

        # Update appropriate value for given attribute in BCN object
        if self.diffType == "Percent":
            self.bcnObj[self.varName] *= (self.diffValue + 100)/100

        elif self.diffType == "Gross":
            # self.bcnObj[self.varName]
            # Calculate gross change 
            pass

        else:
            logger.warning("Warning: %s", "Difference type is unrecognized. No change was made")

        # Rerun analysis with updated values, store output
        # E.g. new_output = cost_function(a', b', c')
        # (sensitivity summary)

        # Revert BCN values 
        self.bcnObj = original_val

    