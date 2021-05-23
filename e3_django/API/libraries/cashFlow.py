"""
Purpose: The CashFlow Library derives the cash flows for individual BCNs and the total
cash flows for alternatives, ultimately constructing the Total Cash Flows objects.
"""
# import files
from . import discounting as discounting

def blankFlow(studyPeriod, timestepValue):
    """
    Purpose: Initializes a blank cash flow list to store data
    """
    timestepCount = studyPeriod / timestepValue
    arr = [0] * (timestepCount + 1)
    return arr


def bcnFlow(discountRate, bcnObject, studyPeriod, timestepCount):
    """
    Purpose: Begins construction of cash flows for a given BCN
    """
    if not bcnObject.recurBool:
        bcnFlowNonRecur(bcnObject, discountRate, studyPeriod, timestepCount)
    else:
        bcnFlowRecur(bcnObject, discountRate, studyPeriod, timestepCount)


def bcnFlowNonRecur(discountRate, bcnObject, studyPeriod, timestepValue):
    """
    Purpose: Completes construction of flows for non-recurring BCNs
    """
    bcnFlowNonDisc = blankFlow(studyPeriod, timestepValue)
    bcnFlowDisc = blankFlow(studyPeriod, timestepValue)
    quantList = blankFlow(studyPeriod, timestepValue)

    if not bcnObject.valuePerQ:
        return bcnFlowNonDisc, bcnFlowDisc

    if bcnObject.quantVarValue:
        quantEsc = discounting.quantEscalationCalc(quantVarRateType, quantVarValue, initialOcc)

        return bcnFlowNonDisc, bcnFlowDisc, quantList

    return


def bcnFlowRecur(discountRate, bcnObject, timestep):
    """
    Purpose: Completes construction of flows for recurring BCNs
    """
    bcnFlowNonDisc = blankFlow(studyPeriod, timestepValue)
    bcnFlowDisc = blankFlow(studyPeriod, timestepValue)
    recurList = blankFlow(studyPeriod, timestepValue)
    quantList = blankFlow(studyPeriod, timestepValue)


def rvCalc(bcnObject, value, timestep=None):
    """
    Purpose: Calculates the residual values of a BCN
    """
    pass

def totalFlows(bcnObjectList, altID):
    """
    Purpose: Calculates the total flows for an alternative
    """
    pass