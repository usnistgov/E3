from typing import Union

import numpy

from API.objects import RequiredCashFlow
from API.serializers import CostType


def net_benefits(benefits: CostType, costs: CostType, benefits_base: CostType, costs_base: CostType) -> CostType:
    return (benefits - benefits_base) / (costs - costs_base)


def net_savings(costs: CostType, costs_base: CostType) -> CostType:
    return costs - costs_base


def bcr(benefits: CostType, costs_inv: CostType, costs_inv_base: CostType) -> Union[CostType, str]:
    """
    Calculate Benefit-cost Ratio (BCR).

    :param benefits:
    :param costs_inv:
    :param costs_inv_base:
    :return: The calculated BCR.
    """
    return check_fraction(benefits, costs_inv - costs_inv_base)


def sir(costs_inv: CostType, costs_non_inv: CostType, costs_inv_base: CostType, costs_non_inv_base: CostType) \
        -> Union[CostType, str]:
    """
    Calculate Saving to Investment Ratio (SIR)

    :param costs_inv:
    :param costs_non_inv:
    :param costs_inv_base:
    :param costs_non_inv_base:
    :return: The calculated SIR.
    """
    return check_fraction(costs_non_inv_base - costs_non_inv, costs_inv_base - costs_inv)


def check_fraction(numerator: CostType, denominator: CostType) -> Union[CostType, str]:
    """
    Checks that the given numerator and denominator are valid, otherwise a string is returned that is either
    "Infinity" or "Not Calculable".

    :param numerator: The numerator of the fraction.
    :param denominator: The denominator of the fraction.
    :return: The calculated fraction or "Infinity" or "Not Calculable".
    """
    if denominator > 0 and numerator > 0:
        return numerator / denominator
    elif denominator <= 0 and numerator > 0:
        # FIXME: Need to come up with a better tolerance here to avoid divide by zero error
        return "Infinity"
    elif denominator <= 0 and numerator <= 0:
        return "Not Calculable"


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


def payback_period(tot_costs, tot_benefits):  # used for both simple and discounted payback
    if len(tot_costs) != len(tot_benefits):
        raise ValueError("Total Costs and Total Benefits must be the same length.")

    for i in range(len(tot_costs)):
        if numpy.subtract(tot_costs[i], tot_benefits[i]) <= 0:
            return i


class AlternativeSummary:
    def __init__(self, alt_id, reinvest_rate, study_period, marr, flow: RequiredCashFlow,
                 baseline: "AlternativeSummary" = None, irr: bool = False):
        self.altID = alt_id

        self.totalBenefits = sum(flow.totBenefitsDisc)
        self.totalCosts = sum(flow.totCostDisc)
        self.totalCostInv = sum(flow.totCostsDiscInv)
        self.totalCostsNonInv = sum(flow.totCostsNonDiscInv)

        self.netBenefits = net_benefits(self.totalBenefits, self.totalCosts, baseline.totalBenefits,
                                        baseline.totalCosts) if baseline else None
        self.netSavings = net_savings(self.totalCosts, baseline.totalCosts) if baseline else None
        self.SIR = sir(self.totalCostInv, self.totalCostsNonInv, baseline.totalCostInv,
                       baseline.totalCostsNonInv) if baseline else None
        self.IRR = numpy.irr(self.totFlowsNonDisc) if irr else None
        self.AIRR = airr(self.SIR, self.reinvest_rate, study_period)
        self.SPP = payback_period(flow.totCostNonDisc, flow.totBenefitsNonDisc)
        self.DPP = payback_period(flow.totCostDisc, flow.totBenefitsDisc)
        self.BCR = bcr(self.netSavings, self.totalCostInv, baseline.totalCostInv)

        self.quantSum = None
        self.quantUnits = None

        self.MARR = marr

        self.deltaQuant = None
        self.nsDeltaQuant = None
        self.nsElasticityQuant = None
