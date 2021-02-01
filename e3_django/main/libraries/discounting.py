"""
Purpose: The Discounting Library serves two purposes.
1. Discounts cash flows back to present value
2. Provides a check that all required information for discounting is present in the user input.
"""
# import files

def inflationRateCalc(dRateNorm, dRateReal):
    """
    Purpose: Returns inflation rate from nominal and real discount rates, 
    if user fails to provide an inflation rate.
    """
    inflation_rate = (1+dRateNorm) / (1+dRateReal) - 1
    return inflation_rate


def dRateNomCalc(inflationRate, dRateReal):
    """
    Purpose: Returns the nominal discount rate from inflation and real discount rates,
    if user fails to provide a nominal discount rate.
    """
    dRateNorm = (1 + inflationRate) * (1 + dRateReal) - 1
    return dRateNorm


def dRateRealCalc(dRateNorm, inflationRate): 
    """
    Purpose: Returns the real discount rate from inflation and nominal discount rates,
    if user fails to provide real discount rate.
    """
    dRateReal = (1 + dRateNorm) / (1 + inflationRate) - 1
    return dRateReal


def recurEscalationRateCorrection(analysisType, recurrenceVariabilityRateType, recurrenceVariabilityRateValues, \
    time = None): #! do we need inflationRate as input? <- A: probably a global var.
                # realdiscountrate, nominaldiscountrate, inflationrate <- from Analysis Class. Higher lvl variables that are independent (above) all
    """
    Purpose: Returns the escalation rate, when there is a discrepancy between 
    chosen analysis and provided escalation rates.
    Note: Escalation rate is for nominal, but analysis is in real dollars - or vice versa.
    """
    # TODO: if escalation rate is required to be in real dollars: <- 'Escalation rate': rate at which cost that is recurring over time. (how price is changing over time)
    # 'escalation rate' depends on BCN benefit or cost value  == 'recurrence' parameters from the BCN Object
        if isinstance(recurrenceVariabilityRateValues, float):
            e = (1 + recurrenceVariabilityRateValues) / (1 + inflationRate) - 1
            return e
        
        elif isinstance(recurrenceVariabilityRateValues, list) and all(isinstance(x, float) for x in \
            recurrenceVariabilityRateValues) and time: # time input required
            # for x, i in enumerate(recurrenceVariabilityRateValues):
                # x = (1 + recurrenceVariabilityRateValues[i]) / (1 + inflationRate) - 1
            e_time = (1 + recurrenceVariabilityRateValues[time]) / (1 + inflationRate) - 1
            return e_time

    # TODO: elif escalation rate is required to be in nominal dollars:
        if instance(recurrenceVariabilityRateValues, float):
            E = (1 + I) * (1 + recurrenceVariabilityRateValues) - 1
            return E
        elif isinstance(recurrenceVariabilityRateValues, list) and all(isinstance(x, float) for x in \
            recurrenceVariabilityRateValues) and time: # time input required
            E_time = (1 + I) * (1 + recurrenceVariabilityRateValues[time]) - 1

        return E_time


def quantEscalationCalc(quantityVariabilityRateType, quantityVariabilityRateValues, time): #! do we need recurrenceVariabilityRateValues as input?
    """
    Purpose: Return escalation rate to use for a quantity type BCN object provided that
    a quantityVariabilityRateType value exists, otherwise it is assumes no escalation occurs 
    for the quantity.
    """
    if isinstance(quantityVariabilityRateValues, float):
        e = (1 + quantityVariabilityRateValues) / 1 - 1
    elif isinstance(quantityVariabilityRateValues, list) and all(isinstance(x, float) for x in \
        quantityVariabilityRateValues) and time: # time input is required
        e = (1 + recurrenceVariabilityRateValues[time]) / 1 - 1  
    return e 


def spv(recurrenceVariabilityRateValues, discountRate, time): # 
    """
    Purpose: Return multiplier to convert a future value to present value.
    """
    if isinstance(recurrenceVariabilityRateValues, float):
        SPV = (1 + recurrenceVariabilityRateValues)^time / (1 + discountRate)^time
    elif isinstance(recurrenceVariabilityRateValues, list) and all(isinstance(x, float) for x in \
        recurrenceVariabilityRateValues):
        prod = 1
        for i in range(1, time + 1): #! what is unit for time? (currently assumed as int) A: 'time' is an int type. can either be year, or combination of YMD
            prod *= (1 + recurrenceVariabilityRateValues[i])

        SPV = 1 / (1 + discountRate) * prod
        return SPV

def discValueCalc(value, spv): #! do we need time as input? A: 'value' is from BCN Class <- Josh & David will discuss. may have to include some var.
    # Probably: initial recurrence should be added to the BCN Class.
    #? if there exist no instance where we need spv value w/o calling SPV, then we may fold spv() & discValueCalc() into single function
    discValue = spv[time] * value # dateOfOccurence from BCN OBject
    return discValue

# ! Inconsistent documentation - should we include presentValueCalc() & escalatedQuantCalc specified in functions?
"""
def presentValueCalc(value, spv):
    #Purpose: Return present value of a cash flow at set timestep.
    
    return 
"""

def escalatedQuantCalc(quantity, quantityVariabilityRateType, quantityVariabilityRateValues, time):
    """
    Purpose: Return escalated value of a non-monetary quantity.
    """
    if isinstance(quantityVariabilityRateValues, float):
        mult = (1 + quantityVariabilityRateValues)^time / 1
    elif isinstance(quantityVariabilityRateValues, list) and all(isinstance(x, float) for x in \
        quantityVariabilityRateValues) and time: # time input is required
        mult = 1
        for i in range(1, time+1): #! what is unit for time? (currently assumed as int) A. Yes time is always 'int' type.
            mult *= (1 + quantityVariabilityRateValues[i])

        escQuantVal = mult * quantity
    
    return escQuantVal


