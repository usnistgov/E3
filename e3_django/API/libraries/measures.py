from django.db import models
import numpy as np


def checkCosts(totCostDisc, totCostDiscInv, totCostDiscNonInv):
    ## Should be run after sumCosts through sumBenefits
    if totCostDisc != totCostDiscInv + totCostDiscNonInv:
        raise Exception("There was an error in calculation")

    return


def sumCosts(totCostDisc):
    return np.sum(totCostDisc)


def sumBenefits(totBenefitsDisc):
    return np.sum(totBenefitsDisc)


def sumInv(totCostsInvDisc):
    return np.sum(totCostsInvDisc)


def sumNonInv(totCostsNonInvDisc):
    return np.sum(totCostsNonInvDisc)


def netBenefits(totalBenefits, totalCosts, totalBenefitsBase, totalCostsBase):
    return (totalBenefits - totalBenefitsBase) - (totalCosts - totalCostsBase)


def netSavings(totalCosts, totalCostsBase):
    return (totalCostsBase - totalCosts)


def measBCR(netBenefits, totalCostsInv, totalCostsInvBase):
    numerator = netBenefits  ## I know this isn't really a simplification, however it makes the logic that follow easier to understand
    denominator = totalCostsInv - totalCostsInvBase
    if denominator <= 0 and numerator > 0:
        bcr = 'Infinity'
    elif denominator <= 0 and numerator <= 0:
        bcr = "Not Calculable"
    else:
        bcr = numerator / denominator
    return bcr


def measSIR(totalCostsInv, totalCostsNonInv, totalCostsInvBase, totalCostsNonInvBase):
    numerator = (totalCostsNonInvBase - totalCostsNonInv)
    denominator = (totalCostsInvBase - totalCostsInv)
    if denominator <= 0 and numerator > 0:
        sir = 'Infinity'
    elif denominator <= 0 and numerator <= 0:
        sir = "Not Calculable"
    else:
        sir = numerator / denominator
    return sir


def measAIRR(sir, reinvestRate, studyPeriod):
    if sir == "Not Calculable" or sir == "Infinity" or sir <= 0:
        return "AIRR Not Calculable"
    if sir > 0:
        return (1 + reinvestRate) * (sir) ** (1 / studyPeriod) - 1


def measDeltaQ(baselineFlow, altFlow):
    return altFlow - baselineFlow


def measNSPerQ(netSavings, deltaQ):
    if deltaQ != 0:
        return netSavings / deltaQ
    else:
        return "Infinity"


def measNSPerPctQ(netSavings, deltaQ, totQBase):
    if deltaQ != 0 and totQBase != 0:
        return netSavings / (deltaQ / totQBase)
    else:
        return "Infinity"


def measNSElasticity(netSavings, totalCosts, deltaQ, totalQBase):
    if deltaQ != 0 and totQBase != 0:
        return (netSavings / totCosts) / (deltaQ / totQBase)
    else:
        return "Infinity"


def measIRR(totCosts, totBenefits):
    totFlows = np.subtract(totCosts, totBenefits)
    """ Note from pseudocode docs: Technically speaking we should be solving this, but the solution requires a 
    root finding algorithm and repeatedly updating cash flows to obtain.
    """
    measIRR = numpy.irr(totFlows)
    return measIRR


def measPaybackPeriod(totCosts, totBenefits):  ## used for both simple and discounted payback
    dpp = "Infinity"
    for i in range(len(totCosts)):
        if np.sum(np.subtract(totCosts[:i + 1], totBenefits[:i + 1])) <= 0:
            dpp = i
            break
    return dpp


##Moved to quantList function
##def totalQuant(self, altID, tag):
##        quantSum = 0
##
##	return quantSum, quantUnits

def calcBaselineMeas(baselineTotFlows,
                     irrBoolean):  ## Still a lot of redundancy in here. Consider adding more granular functions. Same as for the following function
    totFlows = np.subtract(baselineTotFlows.totCostsDisc, baselineTotFlows.totBenefitsDisc)
    totFlowsNonDisc = np.subtract(baselineTotFlows.totCostsNonDisc, baselineTotFlows.totBenefitsNonDisc)
    totCosts = baselineTotFlows.totCostsDisc
    totBens = baselineTotFlows.totBenefitsDisc
    totCostsInv = baselineTotFlows.totCostsInvDisc
    totCostsNonInv = baselineTotFlows.totCostsNonInvDisc
    baselineFlowList = [totFlows, totCosts, totBens, totCostsInv, totCostsNonInv]

    totalCostsBase = sumCosts(totCosts)
    totalBenefitsBase = sumBenefits(totBens)
    totalInvBase = sumInv(totCostsInv)
    totalNonInvBase = sumNonInv(totCostsNonInv)
    if irrBoolean == True:
        irr = measIRR(totFlowsNonDisc)
    else:
        irr = None
    dpp = measPaybackPeriod(totCosts, totBens)
    spp = measPaybackPeriod(baselineTotFlows.totCostsNonDisc,
                            baselineTotFlows.totBenefitsNonDisc)  ## Only call to these two attributes

    baselineMeasList = [baselineID, totalBenefitsBase, totalCostsBase, totalInvBase, totalNonInvBase, None, None, irr,
                        None, dpp, spp, None]

    return baselineFlowList, baselineMeasList


def calcBaselineTagMeas(baselineTagList, altID, tag, flowDisc, totTagQ, units):
    if altID == baselineID and tag not in baselineTagList:  ## Add new tags to baselineTagList
        baselineTagList.append([tag, flowDisc, totTagQ, units])
    elif altID == baselineID and tag in baselineTagList:
        tagIndex = baselineTagList.index(
            tag)  ## If tag exists, add the new values to the previous entries in baselineTagList. These are used for Total Quantity Flows outputs
        baselineTagList[i][1] = np.add(flowDisc, baselineTagList[i][1])
        baselineTagList[i][2] = np.add(totTagQ, baselineTagList[i][2])

    for baselineTag in baselineTagList:
        baselineTag[1] = np.sum(baselineTag[1])
        baselineTag[2] = np.sum(baselineTag[2])

    return baselineTagList


def quantList(baselineTagList):
    quantSum = []
    quantUnits = []
    for i in range(len(baselineTagList)):
        quantSum.append([baselineTagList[i][0], np.sum(baselineTagList[i][2])])
        quantUnits.append([baselineTagList[i][0], baselineTagList[i][3]])

    return quantSum, quantUnits


def calcAltMeas(altID, irrBoolean, baselineFlowList, reinvestRate, studyPeriod, altTotFlows):
    ## Loop through remainder of total Required Flows objects and calculate their measures.
    totFlows = np.subtract(altTotFlows.totCostsDisc, altTotFlows.totBenefitsDisc)
    totFlowsNonDisc = np.subtract(altTotFlows.totCostsNonDisc, altTotFlows.totBenefitsNonDisc)
    totCostFlows = altTotFlows.totCostsDisc
    totBenFlows = altTotFlows.totBenefitsDisc
    totCostInvFlows = altTotFlows.totCostsDiscInv
    totCostNonInvFlows = altTotFlows.totCostsDiscNonInv

    totalCosts = sumCosts(totCostFlows)
    totalBenefits = sumBenefits(totBenFlows)
    totalCostsInv = sumInv(totCostInvFlows)
    totalCostsNonInv = sumNonInv(totCostNonInvFlows)
    if irrBoolean == True:
        irr = measIRR(totFlowsNonDisc)
    else:
        irr = None
    netBenefits = netBenefits(totalBenefits, totalCosts, baselineFlowList[2], baselineFlowList[1])
    netSavings = netSavings(totalCosts, baselineFlowList[1])
    bcr = measBCR(netBenefits, totalCostsInv, baselineFlowList[3])
    sir = measSIR(totalCostsInv, totalCostsNonInv, baselineFlowList[3], baselineFlowList[4])
    airr = measAIRR(sir, reinvestRate, studyPeriod)
    dpp = measPaybackPeriod(totCostFlows, totBenFlows)
    spp = measPaybackPeriod(altTotFlows.totCostsNonDisc, altTotFlows.totBenefitsNonDisc)

    altMeasList = [altID, totalBenefits, totalCosts, totalCostsInv, totalCostsNonInv, netBenefits, netSavings, sir, irr,
                   airr,
                   dpp, spp, bcr]

    return altMeasList


def calcAltTagMeas(totOptFlowsList, altMeasList, baselineTagList):
    altTagList = []
    altTagFlowList = []
    quantMeasList = []
    deltaQuant = []
    nsDeltaQuant = []
    nsPerQuant = []
    nsPerPctQuant = []
    nsElasticityQuant = []
    for totOptFlow in totOptFlowsList:
        if altID == totOptFlow.altID:
            tag = totOptFlow.bcnTag
            totalTagFlow = totOptFlow.totTagFlow
            totTagQ = totOptFlow.totTagQ
            quantUnits = totOptFlow.quantUnits
            if tag not in altTagList:  ## Add new tags to baselineTagList
                altTagList.append(tag)
                altTagFlowList.append([tag, totalTagFlow, totTagQ, quantUnits])
            elif tag in altTagList:
                tagIndex = altTagList.index(
                    tag)  ## If tag exists, add the new values to the previous entries in baselineTagList. These are used for Total Quantity Flows outputs
                altTagFlowList[tagIndex][1] = np.add(totalTagFlow, altTagFlowList[tagIndex][1])
                altTagFlowList[tagIndex][2] = np.add(totTagQ, altTagFlowList[tagIndex][2])

    for altTag in altTagFlowList:
        altTag[1] = np.sum(altTag[1])
        altTag[2] = np.sum(altTag[2])

    for baselineTag in baselineTagList:
        for altTag in altTagFlowList:
            if altTag[0] not in baselineTag:
                deltaQ = altTag[2]
                deltaQuant.append([altTag[0], deltaQ])
                nsPerQuant.append([altTag[0], measures.measNSPerQ(altMeasList[6], baselineTag[2])])
                nsPerPctQuant.append([altTag[0], "Infinite"])
                nsElasticityQuant.append([altTag[0], "Infinite"])
            elif altTag[0] == baselineTag[0]:
                deltaQ = measures.measDeltaQ(baselineTag[2], np.sum(altTag[2]))
                deltaQuant.append([altTag[0], deltaQ])
                nsPerQuant.append([altTag[0], measures.measNSPerQ(altMeasList[6], deltaQ)])
                nsPerPctQuant.append([altTag[0], measures.measNSPerPctQ(altMeasList[6], deltaQ, baselineTag[2])])
                nsElasticityQuant.append(
                    [altTag[0], measures.measNSElasticity(altMeasList[6], altMeasList[2], deltaQ, baselineTag[2])])

    return [deltaQuant, nsPerQuant, nsPerPctQuant, nsElasticityQuant]
