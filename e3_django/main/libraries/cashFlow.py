from main.models.userDefined import alternative, analysis, bcn, scenario, sensitivity


def blankFlow(studyPeriod, timestepValue):
    timestepCount = studyPeriod / timestepValue
    return #zeroes(timestepCount + 1)


def bcnFlow(bcnObject, studyPeriod, timestepCount):
    if bcnObject.recurBool == False:
        bcnFlowNonRecur(bcnObject, discountRate)
    else:
        bcnFlowNonRecur(bcnObject, discountRate)


def bcnFlowNonRecur(bcnObject, discountRate):
    bcnFlowNonDisc = blankFlow(studyPeriod, timestepValue)
    bcnFlowDisc = blankFlow(studyPeriod, timestepValue)
    quantList = blankFlow(studyPeriod, timestepValue)


    if not bcnObject.valuePerQ:
        return bcnFlowNonDisc, bcnFlowDisc
    if bcnObject.quantVarValue:
        return
        # quantEsc = 
    def escalatedQuantCalc(quantity, quantVarRateType, quantVarValue, initialOcc):

        return bcnFlowNonDisc, bcnFlowDisc, quantList

    return


def bcnFlowRecur(bcnObject, discountRate, timestep):
    bcnFlowNonDisc = blankFlow(studyPeriod, timestepValue)
    bcnFlowDisc = blankFlow(studyPeriod, timestepValue)
    recurList = blankFlow(studyPeriod, timestepValue)
    quantList = blankFlow(studyPeriod, timestepValue)

    