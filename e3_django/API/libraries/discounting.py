"""
Purpose: The Discounting Library serves two purposes.
1. Discounts cash flows back to present value
2. Provides a check that all required information for discounting is present in the user input.
"""
# import files
from . import validateRead as vr


def recurEscalationRateCorrection(analysisType, inflationRate, recurrenceVariabilityRateType, recurrenceVariabilityRateValues, time = None): 
    # realdiscountrate, nominaldiscountrate, inflationrate <- from Analysis Class. 
    #Higher lvl variables that are independent (above) all
    """
    Purpose: Returns the escalation rate, when there is a discrepancy between chosen analysis and 
    provided escalation rates.
    Note: Escalation rate is for nominal, but analysis is in real dollars - or vice versa.
    """
    # Note: 'escalation rate' depends on BCN benefit or cost value  == 'recurrence' parameters from the BCN Object

    if analysisType == 'real': 
        if isinstance(recurrenceVariabilityRateValues, float): 
            # if float, time input is not required
            e = (1 + recurrenceVariabilityRateValues) / (1 + inflationRate) - 1

            return e
        
        elif isinstance(recurrenceVariabilityRateValues, list) and all(isinstance(x, float) for x in recurrenceVariabilityRateValues):
            # if list, time input it required
            if not time or (isinstance(time, int) and time <= 0):
                raise Exception("Err: Positive integer time is required for calculation")
            e_time = [0] * (time + 1)

            for i, val in enumerate(recurrenceVariabilityRateValues):
                e_time[i] = (1 + val) / (1 + inflationRate) - 1

            return e_time
        else: raise Exception("Err: Something went wrong. Check quantityVariabilityRateValues or time inputs")


    elif analysisType == 'nominal': 
        if isinstance(recurrenceVariabilityRateValues, float):
            # if float, time input is not required
            E = (1 + inflationRate) * (1 + recurrenceVariabilityRateValues) - 1

            return E
            
        elif isinstance(recurrenceVariabilityRateValues, list) and all(isinstance(x, float) for x in recurrenceVariabilityRateValues):
            # if list, time input is required
            if not time or not isinstance(time, int) or time <= 0:
                raise Exception("Err: Positive integer time is required for calculation")
            E_time = [0] * (time + 1)
            for i, val in enumerate(recurrenceVariabilityRateValues):
                E_time[i] = (1 + inflationRate) * (1 + val) - 1

            return E_time
        else: raise Exception("Err: Something went wrong. Check quantityVariabilityRateValues or time inputs")

    else: raise Exception("Err: analysisType must either be real or nominal")


def quantEscalationCalc(quantityVariabilityRateType, quantityVariabilityRateValues, time=None):
    """
    Purpose: Return escalation rate to use for a quantity type BCN object provided that
    a quantityVariabilityRateType value exists, otherwise it is assumes no escalation occurs 
    for the quantity.
    """
    if isinstance(quantityVariabilityRateValues, float):
        # if float, time input is not required
        e = (1 + quantityVariabilityRateValues) / 1 - 1

    elif isinstance(quantityVariabilityRateValues, list) and all(isinstance(x, float) for x in quantityVariabilityRateValues):
        # if list, time input is required
        if not time or not isinstance(time, int) or time <= 0:
            raise Exception("Err: Positive integer time is required for calculation")

        e_time = [0] * (time + 1)
        for i, val in enumerate(quantityVariabilityRateValues):
            e_time[i] = (1 + val) / 1 - 1

        return e_time
    
    else: raise Exception("Err: Something went wrong. Check quantityVariabilityRateValues or time inputs")


def spv(time, recurrenceVariabilityRateValues, discountRate):
    """
    Purpose: Return multiplier to convert a future value to present value.
    """
    if not time or not isinstance(time, int) or time < 0:
        raise Exception("Err: Positive integer time is required for calculation")

    if isinstance(recurrenceVariabilityRateValues, float):
        SPV = ((1 + recurrenceVariabilityRateValues) ** time) / ((1 + discountRate) ** time)

    elif isinstance(recurrenceVariabilityRateValues, list) and all(isinstance(x, float) for x in recurrenceVariabilityRateValues):
        prod = 1
        for i in range(1, time + 1): 
            prod *= ((1 + recurrenceVariabilityRateValues[i]) ** time)
        SPV = prod / ((1 + discountRate) ** time)

    return SPV 


def discValueCalc(time, value, spv, recurrenceVariabilityRateValues):
    # 'value' is from BCN Class <- Josh & David
    # will discuss. may have to include some var. For now, is included as parameter; remove as necessary. Initial
    # recurrence probably should be added to the BCN Class. Note: if there exist NO instance where we need spv value
    # w/o calling SPV, then we may fold spv() & discValueCalc() into single function.
    if not time or time < 0:
        raise Exception("Time value must be supplied, and be positive")

    discValue = spv[time] * value # dateOfOccurence from BCN OBject
    return discValue


def escalatedQuantCalc(quantity, quantityVariabilityRateType, quantityVariabilityRateValues, time=None):
    """
    Purpose: Return escalated value of a non-monetary quantity.
    """
    if isinstance(quantityVariabilityRateValues, float):
        prod = ((1 + quantityVariabilityRateValues) ** time) / 1

    elif isinstance(quantityVariabilityRateValues, list) and all(isinstance(x, float) for x in quantityVariabilityRateValues):
        prod = 1
        for i in range(1, time + 1):
            prod *= (1 + quantityVariabilityRateValues[i])
        escQuantVal = prod * quantity
    
    return escQuantVal
