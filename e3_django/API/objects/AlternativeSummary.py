from typing import Union

import numpy

from API.objects import RequiredCashFlow, OptionalCashFlow
from API.variables import CostType


def net_benefits(benefits: CostType, costs: CostType, benefits_base: CostType, costs_base: CostType) -> CostType:
    return (benefits - benefits_base) - (costs - costs_base)


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


def sir(costs_non_inv_base: CostType, costs_non_inv: CostType, costs_inv_base: CostType, costs_inv: CostType) \
        -> Union[CostType, str]:
    """
    Calculate Saving to Investment Ratio (SIR)

    :param costs_non_inv_base:
    :param costs_non_inv:
    :param costs_inv_base:
    :param costs_inv:

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
    if denominator <= 0 and numerator > 0:
        # FIXME: Need to come up with a better tolerance here to avoid divide by zero error
        return "Infinity"
    elif denominator <= 0 and numerator <= 0:
        return "Not Calculable"
    else:
        return numerator / denominator


def airr(sir_value: CostType, reinvest_rate: CostType, study_period: int) -> Union[CostType, str]:
    """
    Calculate the adjusted internal rate of return (AIRR).

    :param sir_value:
    :param reinvest_rate:
    :param study_period:
    :return: The calculated AIRR.
    """
    if not isinstance(sir_value, CostType) or sir_value <= CostType(0):
        return "AIRR Not Calculable"

    return (1 + reinvest_rate) * sir_value ** CostType(1 / study_period) - 1


def payback_period(tot_costs, tot_benefits):  # used for both simple and discounted payback
    if len(tot_costs) != len(tot_benefits):
        raise ValueError("Total Costs and Total Benefits must be the same length.")

    for i in range(len(tot_costs)):
        if numpy.subtract(tot_costs[i], tot_benefits[i]) <= 0:
            return i

    return "Infinity"


def ns_per_q(savings: CostType, delta_q: CostType) -> Union[CostType, str]:
    if delta_q == 0:
        return "Infinity"

    return savings / delta_q


def ns_per_pct_q(savings: CostType, delta_q: CostType, total_q_base: CostType) -> Union[CostType, str]:
    if total_q_base == 0:
        return "Infinity"

    return ns_per_q(savings, delta_q / total_q_base)


def ns_elasticity(savings: CostType, total_costs: CostType, delta_q: CostType, total_q_base: CostType) \
        -> Union[CostType, str]:
    if total_costs == 0:
        return "Infinity"

    return ns_per_pct_q(savings / total_costs, delta_q, total_q_base)


# def generate_tag_measures():
#     pass

# def updateMeasure(measureName, flow):
#     """
#     Purpose: Based on measureName (string with the exact same name as the variable without
#     the enclosing brackets if they exist) reset current measure to the input measure.
#     """
#     # if variable name `measureName` exists, resets current measure with input flow.
#     if self.measureName:
#         self.measureName = flow
#
#     return


class AlternativeSummary:
    """
    Represents an alternative summary object with measure in the API output.
    """

    def __init__(self, alt_id, reinvest_rate, study_period, marr, flow: RequiredCashFlow,
                 optionals: list[OptionalCashFlow], baseline: "AlternativeSummary" = None, irr: bool = False):
        self.altID = alt_id
        self.totalBenefits = sum(flow.totBenefitsDisc)
        self.totalCosts = sum(flow.totCostDisc)
        self.totalCostInv = sum(flow.totCostsDiscInv)
        self.totalCostsNonInv = sum(flow.totCostsNonDiscInv)
        self.netBenefits = net_benefits(self.totalBenefits, self.totalCosts, baseline.totalBenefits,
                                        baseline.totalCosts) if baseline else None
        self.netSavings = net_savings(self.totalCosts, baseline.totalCosts) if baseline else None
        self.SIR = sir(baseline.totalCostsNonInv, self.totalCostsNonInv, baseline.totalCostInv, self.totalCostInv) if baseline else None
        self.IRR = numpy.irr(numpy.subtract(flow.totCostDisc, flow.totBenefitsDisc)) if irr else None
        self.AIRR = airr(self.SIR, reinvest_rate, study_period)
        self.SPP = payback_period(flow.totCostNonDisc, flow.totBenefitsNonDisc)
        self.DPP = payback_period(flow.totCostDisc, flow.totBenefitsDisc)
        self.BCR = bcr(self.netSavings, self.totalCostInv, baseline.totalCostInv) if baseline else None

        self.quantSum = calculate_quant_sum(optionals)
        self.quantUnits = calculate_quant_units(optionals)

        self.MARR = marr

        self.deltaQuant = calculate_delta_quant(optionals, baseline.totalCosts if baseline else CostType(0))
        self.nsPercQuant = calculate_ns_perc_quant(self.netSavings, optionals, baseline)
        self.nsDeltaQuant = calculate_ns_delta_quant(self.netSavings, self.deltaQuant, optionals, baseline)
        self.nsElasticityQuant = calculate_ns_elasticity_quant(self.netSavings, self.deltaQuant, self.totalCosts,
                                                               optionals, baseline)


def calculate_quant_sum(optionals):
    return [sum(optional.totTagQ) for optional in optionals]


def calculate_quant_units(optionals):
    return [(optional.tag, optional.quantUnits) for optional in optionals]


def calculate_delta_quant(optionals, baseline_total_cost: CostType = CostType(0)):
    return [optional.totTagQ - baseline_total_cost for optional in optionals]


def calculate_ns_perc_quant(savings, optionals, baseline):
    return [(optional.tag, ns_per_q(savings, optional.totTagQ) if baseline else optional.totTagQ) for optional in optionals]


def calculate_ns_delta_quant(savings, delta_q, optionals, baseline):
    return [(optional.tag, ns_per_pct_q(savings, delta_q, baseline.totalCosts) if baseline else "Infinity") for optional, delta_q in zip(optionals, delta_q)]


def calculate_ns_elasticity_quant(savings, delta_q, total_costs, optionals, baseline):
    return [(optional.tag, ns_elasticity(savings, total_costs, delta_q, baseline.totalCosts) if baseline else "Infinity") for optional, delta_q in zip(optionals, delta_q)]
