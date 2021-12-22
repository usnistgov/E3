from typing import Union, Tuple, Iterable, List, Dict

import numpy

from API.variables import CostType
from compute.objects import RequiredCashFlow, OptionalCashFlow

# Static Variables
ZERO = CostType("0")

# Types
TagMeasure = List[Tuple[str, Union[CostType, str]]]
BaselineTag = Dict[str, CostType]


def net_benefits(benefits: CostType, costs: CostType, benefits_base: CostType, costs_base: CostType) -> CostType:
    """
    Calculates the net benefits.

    :param benefits: The total benefits for this alternative.
    :param costs: The total costs for this alternative.
    :param benefits_base: The total benefits for the baseline alternative.
    :param costs_base: The total costs for the baseline alternative.
    :return: Net benefits.
    """
    return (benefits - benefits_base) - (costs - costs_base)


def net_savings(costs_baseline: CostType, costs: CostType) -> CostType:
    """
    Calculates the net savings.

    :param costs_baseline: Total costs for the baseline alternative.
    :param costs: Total costs for this alternative.
    :return: Net savings.
    """
    return costs_baseline - costs


def bcr(benefits: CostType, costs_inv: CostType, costs_inv_base: CostType, costs_non_inv: CostType,
        costs_non_inv_base: CostType) -> CostType:
    """
    Calculate Benefit-cost Ratio (BCR).

    :param costs_non_inv_base: The total costs non-invest for the baseline alternative.
    :param costs_non_inv: The total costs non-invest for this alternative.
    :param benefits: The net benefits of this alternative.
    :param costs_inv: The total costs invest of this alternative.
    :param costs_inv_base: The total costs invest of the baseline alternative.
    :return: The calculated BCR.
    """
    return check_fraction(benefits, (costs_inv - costs_inv_base) + (costs_non_inv - costs_non_inv_base))


def sir(costs_non_inv_base: CostType, costs_non_inv: CostType, costs_inv: CostType, costs_inv_base: CostType) \
        -> CostType:
    """
    Calculate Saving to Investment Ratio (SIR)

    :param costs_non_inv_base: The total costs non invest of the baseline alternative.
    :param costs_non_inv: The total costs not invest of this alternative.
    :param costs_inv: The total costs invest of this alternative.
    :param costs_inv_base: The total costs invest of the baseline alternative.

    :return: The calculated SIR.
    """
    return check_fraction(costs_non_inv_base - costs_non_inv, costs_inv - costs_inv_base)


def check_fraction(numerator: CostType, denominator: CostType) -> CostType:
    """
    Checks that the given numerator and denominator are valid, otherwise a string is returned that is either
    "Infinity" or "Not Calculable".

    :param numerator: The numerator of the fraction.
    :param denominator: The denominator of the fraction.
    :return: The calculated fraction or "Infinity" or "Not Calculable".
    """
    if denominator <= 0 and numerator > 0:
        return CostType("Infinity")
    elif denominator <= 0 and numerator <= 0:
        return CostType("NAN")
    else:
        return numerator / denominator


def airr(sir_value: CostType, reinvest_rate: CostType, study_period: int) -> CostType:
    """
    Calculate the adjusted internal rate of return (AIRR).

    :param sir_value:
    :param reinvest_rate:
    :param study_period:
    :return: The calculated AIRR.
    """
    if sir_value is None or sir_value.is_nan() or sir_value.is_infinite() or sir_value <= CostType(0):
        return CostType("NAN")

    return (1 + reinvest_rate) * sir_value ** CostType(1 / study_period) - 1


def payback_period(benefits, baseline_benefits, baseline_costs, costs):
    """
    Finds the year in which benefits sum exceeds costs sum. Parameter lists must be the same length. If benefits never
    exceeds costs, "Infinity" will be returned.

    :param benefits: List of benefits for this alternative.
    :param baseline_benefits: List of benefits for the baseline alternative.
    :param baseline_costs: List of costs for the baseline alternative.
    :param costs: List of costs for this alternative.
    :return: The year in which benefits exceeds costs or "Infinity" if benefits never exceeds costs.
    """
    length = len(benefits)
    for flow in [benefits, baseline_benefits, baseline_costs, costs]:
        if len(flow) != length:
            raise ValueError(
                f"Calculation of payback period requires all cash flows to be of the same length. Given:"
                f"\n{benefits}\n{baseline_benefits}\n{baseline_costs}\n{costs}"
            )

    accumulator = 0
    for i, (benefit, baseline_benefit, baseline_cost, cost) in \
            enumerate(zip(benefits, baseline_benefits, baseline_costs, costs)):
        accumulator += (benefit - baseline_benefit) - (baseline_cost - cost)

        if accumulator <= 0:
            return CostType(i)

    return CostType("Infinity")


def ns_per_q(savings: CostType, delta_q: CostType) -> CostType:
    """
    Calculates the ns per q of an optional.

    :param savings: The net savings of this alternative.
    :param delta_q: The delta quantity of an optional.
    :return: The ns per q of an optional.
    """
    if delta_q == 0:
        return CostType("Infinity")

    return savings / delta_q


def ns_per_pct_q(savings: CostType, delta_q: CostType, total_q_base: CostType) -> CostType:
    """
    Calculates the ns per percent q of an optional.

    :param savings: The net savings of this alternative.
    :param delta_q: The delta quantity of an optional.
    :param total_q_base: Total quantities of the baseline alternative.
    :return: The ns per percent q of an optional.
    """
    if total_q_base == 0:
        return CostType("Infinity")

    return ns_per_q(savings, delta_q / total_q_base)


def ns_elasticity(savings: CostType, total_costs: CostType, delta_q: CostType, total_q_base: CostType) -> CostType:
    """
    Calculates the ns elasticity of an optional.

    :param savings: The net savings of this alternative.
    :param total_costs: Teh total costs of this alternative.
    :param delta_q: The delta q of this optional.
    :param total_q_base: The total q of the baseline alternative.
    :return: The ns elasticity of an optional.
    """
    if total_costs == 0:
        return CostType("Infinity")

    return ns_per_pct_q(savings / total_costs, delta_q, total_q_base)


def calculate_tag_cash_flow_sum(optionals: Iterable[OptionalCashFlow]) -> Dict[str, CostType]:
    """
    Calculates the sum of cash flows for tags.

    :param flows: The list of flows to calculate aggregate sum for.
    :return: A dict of the flow tag to its aggregate sum.
    """
    return {optional.tag: sum(optional.totTagFlowDisc) for optional in optionals}


def calculate_quant_sum(optionals: Iterable[OptionalCashFlow]) -> Dict[str, CostType]:
    """
    Calculates the quantity sums of the given optionals.

    :param optionals: The list of optionals to calculate quantity sums for.
    :return: A dict of the optional tag to its quantity sum.
    """
    return {optional.tag: sum(optional.totTagQ) for optional in optionals}


def calculate_quant_units(optionals: Iterable[OptionalCashFlow]) -> Dict[str, str]:
    """
    Reports the quantity units for each of the given optionals.

    :param optionals: The list of optionals to report units for.
    :return: A dict of the optional tag to its quantity unit.
    """
    return {optional.tag: optional.quantUnits for optional in optionals}


def calculate_delta_quant(optionals: Iterable[OptionalCashFlow], baseline: BaselineTag) -> Dict[str, CostType]:
    """
    Calculates the delta quantities for the given optionals using the given baseline optionals.

    :param optionals: The list of optionals to create delta quantities for.
    :param baseline: A dict of baseline optional tags to their quantities.
    :return: A dict of optional tags to their delta quantities calculated with the baseline quantities.
    """
    return {optional.tag: sum(optional.totTagQ) - baseline.get(optional.tag, ZERO) if baseline else ZERO
            for optional in optionals}


def calculate_ns_perc_quant(savings: CostType, optionals: Iterable[OptionalCashFlow],
                            baseline: BaselineTag) -> Dict[str, CostType]:
    """
    Calculates ns percent quantities for the given optionals using the given baseline optionals and this altnerative's
    net savings.

    :param savings: The net savings of this alternative.
    :param optionals: A list of optionals to calculate percent quantities for.
    :param baseline: A dict of baseline optional tags to their quantities.
    :return: A dict of optional tags to their ns percent quantities.
    """
    return {optional.tag: ns_per_pct_q(
        savings,
        sum(optional.totTagQ),
        baseline.get(optional.tag, ZERO)
    ) if baseline else sum(optional.totTagQ) for optional in optionals}


def calculate_ns_delta_quant(savings: CostType, delta_q: Dict[str, CostType], optionals: Iterable[OptionalCashFlow]) \
        -> Dict[str, CostType]:
    """
    Calculates ns delta quantities for the given optionals.

    :param savings: The net savings of this alternative.
    :param delta_q: A dict of optional tags to their delta quantities.
    :param optionals: A list of optionals to calculate ns delta quantities for.
    :return: A dict of optional tags to their ns delta quantities.
    """
    return {optional.tag: ns_per_q(savings, delta_q.get(optional.tag, ZERO)) for optional in optionals}


def calculate_ns_elasticity_quant(savings: CostType, total_costs: CostType, optionals: Iterable[OptionalCashFlow],
                                  baseline: BaselineTag) -> Dict[str, CostType]:
    """
    Calculates ns elasticity quantities for the given optionals suing the given baseline optionals.

    :param savings: The net savings of this alternative.
    :param total_costs: The total costs of this alternative.
    :param optionals: A list of optionals to calculate ns elasticity quantities for.
    :param baseline: A dict of baseline optional tags to their quantity sums.
    :return: A dict of optional tags to their elasticity quantities.
    """
    return {optional.tag: ns_elasticity(
        savings,
        total_costs,
        sum(optional.totTagQ),
        baseline.get(optional.tag, ZERO)
    ) if baseline else CostType("Infinity") for optional in optionals}


class AlternativeSummary:
    """
    Represents an alternative summary object with measure in the API output. If no baseline alternative is provided,
    then all fields are calculated as if it were the baseline.
    """

    def __init__(self, alt_id, reinvest_rate, study_period, marr, flow: RequiredCashFlow,
                 optionals: List[OptionalCashFlow], baseline: "AlternativeSummary" = None, irr: bool = False):
        # Maintain reference to flow object for further calculations.
        # Note: Not included in output, only for internal calculations.
        self.flow = flow

        # Alternative ID
        self.altID = alt_id

        # Sum of cash flow benefits
        self.totalBenefits = sum(flow.totBenefitsDisc)

        # Sum of cash flow costs
        self.totalCosts = sum(flow.totCostDisc)

        # Sum of cash flow discounted, invested costs
        self.totalCostsInv = sum(flow.totCostsDiscInv)

        # Sum of cash flow discounted, non-invested costs
        self.totalCostsNonInv = sum(flow.totCostDiscNonInv)

        # Sum of cash flows by tag
        self.totTagFlows = calculate_tag_cash_flow_sum(optionals)

        # Net benefits between this alternative and the baseline. None if no baseline is provided.
        self.netBenefits = net_benefits(self.totalBenefits, self.totalCosts, baseline.totalBenefits,
                                        baseline.totalCosts) if baseline else None

        # Net savings between this alternative and the baseline. Noe if no baseline is provided.
        self.netSavings = net_savings(baseline.totalCosts, self.totalCosts) if baseline else None

        # SIR of this alternative. None if no baseline is provided.
        self.SIR = sir(baseline.totalCostsNonInv, self.totalCostsNonInv, self.totalCostsInv,
                       baseline.totalCostsInv) if baseline else None

        # IRR Of this alternative. Calculated using numpy. None if IRR is not requested by user.
        self.IRR = numpy.irr(numpy.subtract(flow.totCostDisc, flow.totBenefitsDisc)) if irr else None

        # AIRR of this alternative.
        self.AIRR = airr(self.SIR, reinvest_rate, study_period)

        # Non-discount Payback Period. "Infinity" if no baseline is provided.
        self.SPP = payback_period(
            flow.totBenefitsNonDisc,
            baseline.flow.totBenefitsNonDisc,
            baseline.flow.totCostNonDisc,
            flow.totCostNonDisc
        ) if baseline else CostType("Infinity")

        # Discounted Payback Period. "Infinity" if no baseline is provided.
        self.DPP = payback_period(
            flow.totBenefitsDisc,
            baseline.flow.totBenefitsDisc,
            baseline.flow.totCostDisc,
            flow.totCostDisc,
        ) if baseline else CostType("Infinity")

        # BCR of this alternative. None if not baseline is provided.
        self.BCR = bcr(self.netBenefits, self.totalCostsInv, baseline.totalCostsInv,
                       self.totalCostsNonInv, baseline.totalCostsNonInv) if baseline else None

        # Dictionary of optional tags to quantity sums.
        self.quantSum = calculate_quant_sum(optionals)

        # Dictionary of optional tags to quantity units.
        self.quantUnits = calculate_quant_units(optionals)

        # MARR of the analysis.
        self.MARR = marr

        # Dictionary of optional tags to delta quantities. None if no baseline is provided.
        self.deltaQuant = calculate_delta_quant(optionals, baseline.quantSum) if baseline else None

        # Dictionary of optional tags to ns percent quantities, None if no baseline is provided.
        self.nsPercQuant = calculate_ns_perc_quant(self.netSavings, optionals, baseline.quantSum) if baseline else None

        # Dictionary of optional tags to ns delta quantities. None if no baseline is provided.
        self.nsDeltaQuant = calculate_ns_delta_quant(self.netSavings, self.deltaQuant, optionals) if baseline else None

        # Dictionary of optional tags to ns elasticity quantities. None if no baseline is provided.
        self.nsElasticityQuant = calculate_ns_elasticity_quant(self.netSavings, self.totalCosts, optionals,
                                                               baseline.quantSum) if baseline else None
