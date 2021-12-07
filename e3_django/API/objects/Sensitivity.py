import logging

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
        # Store original bcn object
        original_bcn = self.bcnObj

        # Update appropriate value for given attribute in BCN object
        if self.diffType == "Percent":
            # Update bcn object's specified variable with a Percent change
            self.bcnObj[self.varName] *= (self.diffValue + 100) / 100

        elif self.diffType == "Gross":
            # Update bcn object's specified variable with a Gross change
            self.bcnObj[self.varName] += self.diffValue

        else:
            logger.warning("Warning: %s", "Difference type is unrecognized. No change was made")

        new_bcn = self.bcnObj
        # Revert BCN values 
        self.bcnObj = original_bcn

        return new_bcn