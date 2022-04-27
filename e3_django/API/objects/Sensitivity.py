import logging
from copy import deepcopy
import math
from decimal import Decimal
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


def validate_time(varName, value, bcnObj, study_period):
    if varName == "initialOcc":
        if bcnObj.recurEndDate and value > bcnObj.recurEndDate and bcnObj.recurBool is True:
            raise ValidationError(
                "initialOcc cannot be greater than recurEndDate after alterations from sensitivity input")
        if value > study_period:
            raise ValidationError(
                "initialOcc cannot be greater than studyPeriod after alterations from sensitivity input")
        if value < 0.0:
            raise ValidationError("initialOcc cannot be negative after alterations from sensitivity input")
    if varName == "recurEndDate":
        if value < bcnObj.initialOcc:
            raise ValidationError(
                "recurEndDate cannot be less than initialOcc after alterations from sensitivity input")
        if value > study_period:
            raise ValidationError(
                "recurEndDate cannot be greater than the studyPeriod after alterations from sensitivity input")
        if value < 0.0:
            raise ValidationError("recurEndDate cannot be negative after alterations from sensitivity input")
    if varName == "bcnLife":
        if value < 1.0:
            raise ValidationError("bcnLife cannot be less than one after alterations from sensitivity input")
    if varName == "recurInterval":
        if value < 1.0:
            raise ValidationError("recurInterval cannot be less than one after alterations from sensitivity input")

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
        # BCN Object Name
        self.bcnObj = bcnObj
        # Variable to be changed
        self.varName = varName
        # Type of change to be made
        self.diffType = diffType
        # Value to be changed by
        self.diffValue = diffValue
    
    def calculateOutput(self, base_input, analysis=None):
        # Store original bcn object
        # original_bcn = deepcopy(self.bcnObj)
        if self.globalVarBool is False or not self.globalVarBool:
            # Find correct BCN object based on BCN ID
            for _id, bcn in enumerate(base_input.bcnObjects):
                if bcn.bcnID == self.bcnID:
                    bcnObj = bcn
                    break
            # Store original value
            original_value = getattr(bcnObj, self.varName)

            # Update appropriate value for given attribute in BCN object
            if self.diffType == "Percent":
                # Update bcn object's specified variable with a Percent change
                # self.bcnObj[self.varName] *= (self.diffValue + 100) / 100
                if self.varName in ["initialOcc", "bcnLife", "recurInterval", "recurEndDate"]:
                    value = Decimal(math.ceil(getattr(bcnObj, self.varName)*(self.diffValue + 100) / 100))
                    validate_time(self.varName, value, bcnObj, base_input.analysisObject.studyPeriod)
                else:
                    value = getattr(bcnObj, self.varName) * (self.diffValue + 100) / 100
            
            elif self.diffType == "Gross":
                # Update bcn object's specified variable with a Gross change
                # self.bcnObj[self.varName] += self.diffValue
                if self.varName in ["initialOcc", "bcnLife", "recurInterval", "recurEndDate"]:
                    value = Decimal(math.ceil(getattr(bcnObj, self.varName) + self.diffValue))
                    validate_time(self.varName, value, bcnObj, base_input.analysisObject.studyPeriod)
                else:
                    value = getattr(bcnObj, self.varName) + self.diffValue

            else:
                logger.warning("Warning: %s", "Difference type is unrecognized. No change was made")

            setattr(bcnObj, self.varName, value)

            # new_bcn = self.bcnObj
            new_bcn = deepcopy(bcnObj)
            # Revert BCN values
            # self.bcnObj = original_bcn
            setattr(bcnObj, self.varName, original_value)

            return new_bcn
        else:
            if analysis.outputRealBool:
                discount_rate_old = getattr(analysis, 'dRateReal')
            else:
                discount_rate_old = getattr(analysis, 'dRateNom')

            if self.diffType == "Percent":
                discount_rate_new = discount_rate_old * (100 + self.diffValue)/100
            else:
                discount_rate_new = discount_rate_old + self.diffValue

            return discount_rate_new
