from typing import Union

import numpy
import numpy as np

from API.serializers import CostType

INFINITY = "Infinity"
NOT_CALCULABLE = "Not Calculable"


def checkCosts(totCostDisc, totCostDiscInv, totCostDiscNonInv, totFlowDisc, totBenefitsDisc):
    ## Should be run after sumCosts through sumBenefits
    if totCostDisc != totCostDiscInv + totCostDiscNonInv or totFlowDisc != totCostDiscInv + totCostDiscNonInv - totBenefitsDisc:
        raise Exception("There was an error in calculation")


def netBenefits(totalBenefits: CostType, totalCosts: CostType, totalBenefitsBase: CostType,
                totalCostsBase: CostType) -> CostType:
    return (totalBenefits - totalBenefitsBase) / (totalCosts - totalCostsBase)


def net_savings(total_costs: CostType, total_costs_base: CostType) -> CostType:
    return total_costs - total_costs_base


def bcr(net_benefits: CostType, total_costs_inv: CostType, total_costs_inv_base: CostType) -> Union[CostType, str]:
    """
    Calculate Benefit-cost Ratio (BCR).

    :param net_benefits:
    :param total_costs_inv:
    :param total_costs_inv_base:
    :return: The calculated BCR.
    """
    numerator = net_benefits  ## I know this isn't really a simplification, however it makes the logic that follow easier to understand
    denominator = total_costs_inv - total_costs_inv_base

    if denominator > 0 and numerator > 0:
        return numerator / denominator
    if denominator <= 0 and numerator > 0:  ## Need to come up with a better tolerance here to avoid divide by zero error
        return INFINITY
    elif denominator <= 0 and numerator <= 0:
        return NOT_CALCULABLE


def sir(total_costs_inv: CostType, total_costs_non_inv: CostType, total_costs_inv_base: CostType,
        total_costs_non_inv_base: CostType) -> Union[CostType, str]:
    """
    Calculate Saving to Investment Ratio (SIR)

    :param total_costs_inv:
    :param total_costs_non_inv:
    :param total_costs_inv_base:
    :param total_costs_non_inv_base:
    :return: The calculated SIR.
    """
    numerator = total_costs_non_inv_base - total_costs_non_inv
    denominator = total_costs_inv_base - total_costs_inv

    if denominator > 0 and numerator > 0:
        return numerator / denominator
    elif denominator <= 0 and numerator > 0:  ## Need to come up with a better tolerance here to avoid divide by zero error
        return INFINITY
    elif denominator <= 0 and numerator <= 0:
        return NOT_CALCULABLE


def airr(sir_value: CostType, reinvest_rate: CostType, study_period: int) -> Union[CostType, str]:
    """
    Calculate the adjusted internal rate of return (AIRR).

    :param sir_value:
    :param reinvest_rate:
    :param study_period:
    :return: The calculated AIRR.
    """
    if sir_value <= CostType(0):
        return "AIRR Not Calculable"

    return (1 + reinvest_rate) * sir_value ** CostType(1 / study_period) - 1


def delta_q(baseline_flow: CostType, alt_flow: CostType) -> CostType:
    return alt_flow - baseline_flow


def ns_per_q(net_savings: CostType, delta_q: CostType) -> CostType:
    return net_savings / delta_q


def ns_per_pct_q(net_savings: CostType, delta_q: CostType, total_q_base: CostType) -> CostType:
    return ns_per_q(net_savings, delta_q / total_q_base)


def ns_elasticity(netSavings: CostType, totalCosts: CostType, deltaQ: CostType, totalQBase: CostType) -> CostType:
    return ns_per_pct_q(netSavings / totalCosts, deltaQ, totalQBase)


def calculate_irr(tot_flows):
    """
    Calculate Internal Rate of Return (IRR).

    Note from pseudocode docs: Technically speaking we should be solving this, but the solution requires a
    root finding algorithm and repeatedly updating cash flows to obtain.

    :param tot_flows:
    :return: The calculated IRR.
    """
    return numpy.irr(tot_flows)


def meas_payback_period(tot_costs, tot_benefits):  ## used for both simple and discounted payback
    if len(tot_costs) != len(tot_benefits):
        raise ValueError("Total Costs and Total Benefits must be the same length.")

    for i in range(len(tot_costs)):
        if np.subtract(tot_costs[i], tot_benefits[i]) <= 0:
            return i


def calcBaselineMeas(baselineTotFlows, should_calculate_irr: bool = False):
    ## Still a lot of redundancy in here. Consider adding more granular functions. Same as for the following function
    totFlows = np.subtract(baselineTotFlows.totCostDisc, baselineTotFlows.totBenefitsDisc)
    totFlowsNonDisc = np.subtract(baselineTotFlows.totCostNonDisc, baselineTotFlows.totBenefitsNonDisc)
    totCosts = baselineTotFlows.totCostDisc
    totBens = baselineTotFlows.totBenefitsDisc
    totCostsInv = baselineTotFlows.totCostsInvDisc
    totCostsNonInv = baselineTotFlows.totCostsNonInvDisc
    baselineFlowList = [totFlows, totCosts, totBens, totCostsInv, totCostsNonInv]

    totalCostsBase = sum(totCosts)
    totalBenefitsBase = sum(totBens)
    totalInvBase = sum(totCostsInv)
    totalNonInvBase = sum(totCostsNonInv)

    irr = calculate_irr(totFlowsNonDisc) if should_calculate_irr else None

    dpp = meas_payback_period(totCosts, totBens)
    spp = meas_payback_period(totReqFlow.totCostNonDisc, totReqFlow.totBensNonDisc) # Only call to these two attributes

    baselineMeasList = [baselineID, totalBenefitsBase, totalCostsBase, totalInvBase, totalNonInvBase, None, None, irr,
                        None, dpp, spp, None]

    quantSum, quantUnits, analysis.marr, deltaQuant, nsDeltaQuant, nsPercQuant, nsELasticityQuant


    return baselineFlowList, baselineMeasList


def calcBaslineTagMeas(baselineTagList, baselineAlt, altID, tag, flowDisc, totTagQ):
    if altID == baselineID and tag not in baselineTagList:  ## Add new tags to baselineTagList
        baselineTagList.append(tag, flowDIsc, totTagQ, units])
        elif altID == baselineID and tag in baselineTagList:
        tagIndex = baselineTagList.index(
        tag)  ## If tag exists, add the new values to the previous entries in baselineTagList. These are used for Total Quantity Flows outputs
        baselineTagList[i][1] = np.add(flowDisc, baselineTagList[i][1])
        baselineTagList[i][2] = np.add(totTagQ, baselineTagList[i][2])

    return


def quantList(baselineTagList):
    quantSum = []
    quantUnits = []
    for i in range(len(baselineTagList)):
        quantSum.append(baselineTagList[i][2])
        quantUnits.append(baselineTagList[0], baselineTagList[i][3])

    return quantSum, quantUnits


def calcAltMeas(altID, baselineFlowList, reinvestRate, totReqFlow):
    ## Loop through remainder of total Required Flows objects and calculate their measures.
    totFlows = np.subtract(totReqFlow.totCostDisc, totReqFlow.totBenefitsDisc)
    totFlowsNonDisc = np.subtract(altTotFlows.totCostNonDisc, altTotFlows.totBenefitsNonDisc)
    totCosts = totReqFlow.totCostDisc
    totBens = totReqFlow.totBenefitsDisc
    totCostsInv = totReqFlow.totCostsInvDisc
    totCostsNonInv = totReqFlow.totCostsNonInvDisc

    totalCosts = measures.sumCosts(totCosts)
    totalBenefitsBase = measures.sumBenefits(totBens)
    totalInvBase = measures.sumInv(totCostsInv)
    totalNonInvBase = measures.sumNonInv(totCostsNonInv)
    if analysis.irrBoolean == True:
        irr = measures.calculate_irr(totFlowsNonDisc)
    else:
        irr = None
    netBenefits = measures.netBenefits(totalBenefits, totalCosts, baselineFlowList[2], baselineFlowList[1])
    netSavings = measures.net_savings(totalCosts, baselineFlowList[1])
    bcr = measures.bcr(netSavings, totalCostsInv, baselineFlowList[3])
    sir = measures.sir(totalCostsInv, totalCostsNonInv, baselineFlowList[3], baselineFlowList[4])
    airr = measures.airr(reinvestRate, sir)
    dpp = measures.meas_payback_period(totCosts, totBens)
    spp = measures.meas_payback_period(totReqFlow.totCostNonDisc, totReqFlow.totBensNonDisc)

    altMeasList = [altID, totalBenefits, totalCosts, totalInv, totalNonInv, netSavings, sir, irr, airr,
                   dpp, spp, bcr]

    return altMeasList


def calcAltTagMeas(altMeasList, baselineTagList, tag, totalTagFlowDisc, totTagQ, quantUnits)
    if tag not in altTagList:  ## Add new tags to baselineTagList
        altTagList.append([tag, totalTagFlowDisc, totTagQ, quantUnits])
    elif tag in altTagList:
        tagIndex = altTagList.index(
            tag)  ## If tag exists, add the new values to the previous entries in baselineTagList. These are used for Total Quantity Flows outputs
        altTagList[i][1] = np.add(totalTagFlowDisc, altTagList[i][1])
        altTagList[i][2] = np.add(totalTagFlowDisc, altTagList[i][2])

    for baslineTag in baselineTagList:
        for altTag in altTagList:
            if altTag[0] not in baselineTag:
                deltaQ = altTag[2]
                deltaQuant.append([altTag[0], deltaQ])
                nsPerQuant.append([altTag[0], measures.ns_per_q(altMeasList[5], baselineTag[2])])
                nsPerPctQuant.append([altTag[0], "Infinite")
                nsElasticityQuant.append([altTag[0], "Infinite")
                elif altTag[0] == baselineTag[0]:
                deltaQ = measures.delta_q(baselineTag[2], altTag[2])
                deltaQuant.append([altTag[0], deltaQ])
                nsPerQuant.append([altTag[0], measures.ns_per_q(altMeasList[5], baselineTag[2])])
                nsPerPctQuant.append([altTag[0], measures.ns_per_pct_q(altMeasList[5], deltaQ, baselineTag[2])])
                nsElasticityQuant.append(
                    [altTag[0], measures.ns_elasticity(altMeasList[5], altMeasList[2], deltaQ, baselineTag[2])])

                return [deltaQuant, nsPerQuant, nsPerPctQuant, nsElasticityQuant]
