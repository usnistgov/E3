"""
Purpose: The CashFlow Library derives the cash flows for individual BCNs and the total
cash flows for alternatives, ultimately constructing the Total Cash Flows objects.
"""
# import files
from . import discounting as discounting
import numpy as  np

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
        bcnFlowNonRecur(discountRate, bcnObject, studyPeriod, timestepCount)
    else:
        bcnFlowRecur(discountRate, bcnObject, timestepCount)


def bcnFlowNonRecur(discountRate, bcnObject, studyPeriod, timestepValue):
    """
    Purpose: Completes construction of flows for non-recurring BCNs
    """
    bcnFlowNonDisc = blankFlow(studyPeriod, timestepValue)
    bcnFlowDisc = blankFlow(studyPeriod, timestepValue)
    quantList = blankFlow(studyPeriod, timestepValue)
    quantity = bcnObject.quant # assigning a new variable to store the bcnObject should add some efficiency as it prevents multiple dictionary lookups

    if not bcnObject.valuePerQ: # Keep this with object call since it will have to be made anyway during assignment to ensure the value isn't blank
        pass
    else:
        valPerQ = bcnObject.valuePerQ
        initOcc = bcnObject.initialOcc
        recurVarValue = bcnObject.recurVarValue
        if bcnObject.quantVarValue:
            quantEsc = discounting.quantEscalationCalc(bcnObject.quantVarRate, bcnObject.quantVarValue, initOcc)
            quantList[timestepValue] = quantEsc*quantity
            value = quantEsc*valPerQ
        else:
            quantList[timestepValue] = quantity
            value = quantity*valPerQ
        if isinstance(recurVarValue,list):
            spvMult = recurVarValue[timestepValue]
        elif isinstance(recurVarValue,int):
            spvMult = recurVarValue
        else:
            spvMult = 0
        discMult = discounting.spv(initOcc,spvMult,discountRate)
        discValue = discounting.discValueCalc(value,discMult)
        bcnFlowNonDisc[timestepValue] = value
        bcnFlowDisc[timestepValue] = discValue

        if bcnObject.rvBool: ## Everything below this will be moved to the rvCalc function eventually
            ## Repeated code in Recurring Flow Calc, move to its own function
            residValue = rvCalc(initOcc, value, studyPeriod, bcnLife)
            if isinstance(recurVarValue, list):
                residVarValue = recurVarValue[studyPeriod]
            elif isinstance(recurVarValue,int):
                residVarValue = recurVarValue
            else:
                residVarValue = 0
            residValueMult = discounting.spv(studyPeriod,residVarValue,discountRate)
            residValueDisc = discounting.discValueCalc(residValue,residValueMult)
            bcnFlowNonDisc[studyPeriod] = bcnFlowNonDisc[studyPeriod] + residValue
            bcnFlowDisc[studyPeriod] = bcnFlowDisc[studyPeriod] + residValueDisc

        return bcnFlowNonDisc, bcnFlowDisc, quantList

    return


def bcnFlowRecur(discountRate, bcnObject, studyPeriod, timestepValue):
    """
    Purpose: Completes construction of flows for recurring BCNs
    """
    bcnFlowNonDisc = blankFlow(studyPeriod, timestepValue)
    bcnFlowDisc = blankFlow(studyPeriod, timestepValue)
    recurList = blankFlow(studyPeriod, timestepValue)
    quantList = blankFlow(studyPeriod, timestepValue)

    initOcc = bcnObject.initialOcc
    increment = bcnObject.recurInterval
    quantity = bcnObject.quant
    end = bcnObject.endDate

    recurList = blankFlow(studyPeriod, timestepValue)
    for i in range(initOcc,studyPeriod,increment):
        recurList[i] = 1
    if not bcnObject.valuePerQ:
        pass
    else:
        valPerQ = bcnObject.valuePerQ
        quantVarValue = bcnObject.quantVarValue
        quantVarRate = bcnObject.quantVarRate
        for i in recurList:
            if bcnObject.quantVarValue:
                if isinstance(quantVarValue,list):
                    spvMult = quantVarValue[i]
                elif isinstance(quantVarValue,int):
                    spvMult = quantVarValue
                else:
                    spvMult = 0
                quantEsc = discounting.quantEscalationCalc(quantVarRate, quantVarValue, i)
                value = quantEsc*valPerQ
                quantList[i] = quantEsc*quantity
                bcnFlowNonDisc[i] = value
            else:
                quantList = [sum(x) for x in zip(recurList*quantity,quantList)]
            if isinstance(recurVarValue,list):
                spvMult = recurVarValue[i]
            elif isinstance(recurVarValue,int):
                spvMult = recurVarValue
            else:
                spvMult = 0
            discMult = discounting.spv(i,spvMult,discountRate)
            discValue = discounting.discValueCalc(bcnFlowNonDisc[i],discMult,recurVarRate)
            bcnFlowDisc[i] = discValue
    if bcnObject.rvBool == True:
        if endDate != None:
            residValue = rvCalc(initOcc, value, studyPeriod, bcnLife=None, recurList=recurList, increment=increment, endDate = endDate)
        else:
            residValue = rvCalc(initOcc, value, studyPeriod, bcnLife=None, recurList=recurList, increment=increment)
        ## Repeated code from NonRecurring Flow Calc, move to its own function
        if isinstance(recurVarValue,list):
            residVarValue = recurVarValue[studyPeriod]
        elif isinstance(recurVarValue,int):
            residVarValue = recurVarValue
        else:
            residVarValue = 0
        residValueMult = discounting.spv(studyPeriod,residVarValue,discountRate)
        residValueDisc = discounting.discValueCalc(residValue,residValueMult)
        bcnFlowNonDisc[studyPeriod] = bcnFlowNonDisc[studyPeriod] + residValue
        bcnFlowDisc[studyPeriod] = bcnFlowDisc[studyPeriod] + residValueDisc
    return bcnFlowNonDisc, bcnFlowDisc, quantList
        
            

def rvCalc(initialOcc, value, studyPeriod, bcnLife=None, recurList=None, increment=None, endDate = None):
    if recurList is None:
        if studyPeriod > bcnLife + initialOcc - 1:
            residValue = 0
        else:
            remainingLife = studyPeriod - (initialOcc + bcnLife) - 1
    else:
        if endDate != None and studyPeriod > bcnLife + endDate - 1:
            remainingLife = 0
        elif endDate != None and studyPeriod > bcnLife + endDate - 1:
            remainingLife = studyPeriod - (endDate + bcnLife) - 1
        else:
            nonZeroIndexList = [i for i, e in enumerate(recurList) if e != 0]
            lastFlow = nonZeroIndexList[-1]
            nextFlow = lastFlow + increment
            remainingLife = nextFlow-studyPeriod-1
    if bcnLife != None:
        return residValue = remainingLife/bcnLife*value
    else:
        return residValue = remainingLife/increment*value
    """
    Purpose: Calculates the residual values of a BCN
    """
    pass

def totalFlows(altID,studyPeriod,timestepValue,baseBool,bcnStorageList):
    """
    Purpose: Calculates the total flows for an alternative
    This one's a bit long and may need to be broken up.
    """
    totCostNonDisc = blankFlow(studyPeriod,timestepValue)
    totCostDisc = blankFlow(studyPeriod,timestepValue)
    totCostNonDiscInv = blankFlow(studyPeriod,timestepValue)
    totCostDiscInv = blankFlow(studyPeriod,timestepValue)
    totCostNonDiscNonInv = blankFlow(studyPeriod,timestepValue)
    totCostDiscNonInv = blankFlow(studyPeriod,timestepValue)
    totBenefitsNonDisc = blankFlow(studyPeriod,timestepValue)
    totBenefitsDisc = blankFlow(studyPeriod,timestepValue)
    totCostDir = blankFlow(studyPeriod,timestepValue)
    totCostInd = blankFlow(studyPeriod,timestepValue)
    totCostExt = blankFlow(studyPeriod,timestepValue)
    totCostDirDisc = blankFlow(studyPeriod,timestepValue)
    totCostIndDisc = blankFlow(studyPeriod,timestepValue)
    totCostExtDisc = blankFlow(studyPeriod,timestepValue)
    totBenefitsDir = blankFlow(studyPeriod,timestepValue)
    totBenefitsInd = blankFlow(studyPeriod,timestepValue)
    totBenefitsExt = blankFlow(studyPeriod,timestepValue)
    totBenefitsDirDisc = blankFlow(studyPeriod,timestepValue)
    totBenefitsIndDisc = blankFlow(studyPeriod,timestepValue)
    totBenefitsExtDisc = blankFlow(studyPeriod,timestepValue)

    ## The logic here isn't complicated but there are a lot of nested ifs here and the function is a bit long.
    ## Eventaully break into separate calls to keep clean, make debugging and maintenance easier, and avoid repeated code phrases.
    ## Uncertainty and Sensitivity are implemented by only selecting the affected alts and using them in the altID list.
    ## At that point we need to add another function which, instead of generating the totalRequiredFlows from scratch, pulls the existing
    ## totalRequiredFlows objects, subtracts out the values stored in the bcnStorage objects, and adds the adjusted values in. This should
    ## avoid any unnecessary recalculation. The only exception will be if the altered value impacts all bcns (uncertainty about the discount rate
    ## for instance) in which case every simulation/sensitvity analysis will require running every bcn from scratch. Right now I plan on making
    ## separate totReqFlow objects for the sensitivity analysis and another set for the uncertainty analysis. These sets would be reused instead
    ## of generating a new set every single sensitiviy analysis or uncertainty simulation to keep overhead small.Same for
    ## totOptFlows.
    tagList = []
    tagFlowList = []
    ## Loop to calculate flows
    for bcnStore in bcnStorageList:   ## this looping should work in django, if now we may have to move to a registry metaclass
        if altID in bcnStore.altID:
            tag = bcnStore.tag if bcnStore.tag != None else tag = None
            flowType = bcnStore.type
            flowNonDisc = bcnStore.bcnNonDiscFlow ## One attribute lookup here to prevent further in the future
            flowDisc = bcnStore.bcnDiscFlow
##                if flowType == 'Cost':
##                    bcnFlowNonDisc = np.add(flowNonDisc,bcnFlowNonDisc)
##                    bcnFlowDisc = np.add(flowDisc,bcnFlowDisc)
##                elif flowType == 'Benefit':
##                    bcnFlowNonDisc = np.subtract(flowNonDisc,bcnFlowNonDisc) ## When adding to flows containing costs and benefits, benefits are subtracted, when added to flows of just benefits they are added.
##                    bcnFlowDisc = np.subtract(flowDisc,bcnFlowDisc)
            totCostNonDisc = np.add(flowNonDisc,totCostNonDisc)
            totCostDisc = np.add(flowDisc,totCostDisc)
            totBenefitsNonDisc = np.add(flowNonDisc,totBenefitsNonDisc)
            totBenefitsDisc = np.add(flowDisc,totBenefitsDisc)                        
            if bcnStore.bcnInvestBool == True:
                totCostNonDiscInv = np.add(flowNonDisc,totCostNonDiscInv)
                totCostDiscInv = np.add(flowDisc,totCostDiscInv)
                totBenefitsNonDiscInv = np.add(flowNonDisc,totBenefitsNonDiscInv)
                totBenefitsDiscInv = np.add(flowDisc,totBenefitsDiscInv)
            else:
                totCostNonDiscNonInv = np.add(flowNonDisc,totCostNonDiscNonInv)
                totCostDiscNonInv = np.add(flowDisc,totCostDiscNonInv)
                totBenefitsNonDiscNonInv = np.add(flowNonDisc,totBenefitsNonDiscNonInv) ## Realistically there should be no investment benefits, this is included to add flexibility in the code and allow the option
                totBenefitsDiscNonInv = np.add(flowDisc,totBenefitsDiscNonInv)
            if bcnStore.subType == 'Direct':
                totCostDir = np.add(flowNonDisc,totCostDir)
                totCostDirDisc = np.add(flowDisc,totCostDirDisc)
                totBenefitsDir = np.add(flowNonDisc,totBenefitsDir)
                totBenefitsDirDisc = np.add(flowDisc,totBenefitsDirDisc)
            elif bcnStore.subType == 'Indirect':
                totCostInd = np.add(flowNonDisc,totCostInd)
                totCostIndDisc = np.add(flowDisc,totCostIndDisc)
                totBenefitsInd = np.add(flowNonDisc,totBenefitsInd)
                totBenefitsIndDisc = np.add(flowDisc,totBenefitsIndDisc)
            else:
                totCostExt = np.add(flowNonDisc,totCostExt)
                totCostExtDisc = np.add(flowDisc,totCostExtDisc)
                totBenefitsExt = np.add(flowNonDisc,totBenefitsExt)
                totBenefitsExtDisc = np.add(flowDisc,totBenefitsExtDisc)
            elif tag != None: ## Non Monetary requires a tag so this should cover Non-Monetary as well
                ## We don't store quantities for non-tagged items since they aren't used in calculation
                quantList = bcnStore.quantList
                units = bcnStore.quantUnits
                if not tagList or tag not in tagList:
                    ## I know I could do this as a list of lists but as a first pass this makes it easier for me to verify
                    ## the index is being pulled correctly. We don't use Non-Discounted Flows for the analysis
                    tagList.append([tag,altID])
                    tagFlowList.append(quantList,flowDisc,units)
                else:
                    for tagName in tagList:
                        if tagName == tag:
                            index = tagList.index(tag)
                            if flowType == 'Cost':
                                tagFLowList[index] = [np.add(flowNonDisc,totFlowList[index][0]),np.add(flowNonDisc,totFlowList[index][1]),units]
                            elif flowType == 'Benefit':
                                tagFLowList[index] = [np.subtract(flowNonDisc,totFlowList[index][0]),np.add(flowNonDisc,totFlowList[index][1]),units]
                            ## For now the type and subtype attributes in the totalOptionalFlows class are not used in calculation
                            ## They exist in case we want to use them in the future or a user wishes to add further calculations that require them                     
            
    ## Construct totReqFlow and totOptFlow objects
    totalRequiredFlows(altID,,baseBool)
    for i in range(len(tagList)):
        totalOptionalFlows(altID,False,False,'Non-Monetary',None,tagList,totFlowList[i][0],tagFlowList[i][1],tagFlowList[i][2])
                    
                    
                    
                    
    
