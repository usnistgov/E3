from rest_framework.fields import ListField
from API.registry import E3ModuleConfig
import math, numpy
from typing import Generator, Sequence, List
from API.objects import Bcn
from decimal import Decimal
import os
from copy import deepcopy

from API.serializers.SensitivitySerializer import SensitivitySerializer
from compute.cashflow.apps import cash_flows
from compute.objects import SensitivitySummary
from compute.optional.apps import calculate_tag_flows
from compute.required.apps import calculate_required_flows
from compute.measures.apps import calculate_alternative_summaries
from API.variables import CostType, FlowType, VAR_RATE_OPTIONS

from API.objects import Input, Output
from API.registry import ModuleGraph
from API.serializers.OutputSerializer import OutputSerializer
from copy import deepcopy

def run(base_input, cash_flow):
    """
    Purpose: Re-runs Analysis with updated values, store output, returns list
    of sensitivity summaries.
    """

    # Generate each Sensitivity object with the base_input, in a Loop:
    res = []
    iteration = 1

    for _id, sensitivity_object in enumerate(base_input.sensitivityObjects):
        # Collect information from analysis object and pull base calculation cash flows
        timestep_comp = base_input.analysisObject.timestepComp
        analysis = base_input.analysisObject

        if sensitivity_object.globalVarBool is False or not sensitivity_object.globalVarBool:
            # Get discount rate and generate updated BCN object for altered variable
            discount_rate = analysis.dRateReal if analysis.outputRealBool else analysis.dRateNom
            new_bcn = sensitivity_object.calculateOutput(base_input)
            # Pull BCN object based on bcnID defined by sensitivity object
            for _id, bcn in enumerate(base_input.bcnObjects):
                if bcn.bcnID == sensitivity_object.bcnID:
                    bcnObj = bcn
                    break
            # Remove unaltered cash flow for BCN object from cash_flow
            cash_flow.pop(bcnObj)
            # Update cash flows with altered BCN object flows
            cash_flow[new_bcn] = cash_flows(new_bcn, analysis.studyPeriod, discount_rate, timestep_comp)
            # Set globalVar to false (used as output in sensitivitySummary object)
            globalVar = False
        else:
            # If global we are currently only dealing with the discount rate, clear cash_flow
            # Get new discount rate
            discount_rate = sensitivity_object.calculateOutput(base_input, analysis)
            # Recreate cash flows for all BCNs and populate the empty cash_flow object
            for _id, bcn in enumerate(base_input.bcnObjects):
                cash_flow.pop(bcn)
                cash_flow[bcn] = cash_flows(bcn, analysis.studyPeriod, discount_rate, timestep_comp)
            # Set globalVar to true (used as output in sensitivitySummary object)
            globalVar = True

        # Calculate updated OptionalSummary
        new_optional_summary = calculate_tag_flows(cash_flow, base_input, cash_flow.keys())

        # Calculate updated FlowSummary
        print(discount_rate)
        new_required_summary = calculate_required_flows(cash_flow.keys(), analysis.studyPeriod, cash_flow)

        # Calculate updated MeasureSummary
        new_measure_summary = list(calculate_alternative_summaries(analysis,
                                                                   new_required_summary, new_optional_summary,
                                                                   base_input.alternativeObjects))

        # generate sensitivitySummary
        sensSumm = SensitivitySummary(globalVar, sensitivity_object.bcnObj, sensitivity_object.varName,
                                      sensitivity_object.diffType, sensitivity_object.diffValue,
                                      numpy.sign(sensitivity_object.diffValue), new_measure_summary)
        # Add sensitivity summary to collection of all objects of the same kind
        res.append(sensSumm)
        # Clean up alterations
        if sensitivity_object.globalVarBool is False or not sensitivity_object.globalVarBool:
            # Remove updated BCN, recalculate original BCN and add back to cash_flow
            cash_flow.pop(new_bcn)
            cash_flow[bcnObj] = cash_flows(bcnObj, analysis.studyPeriod,
                                           discount_rate, timestep_comp)
        else:
            # Clear entire cash_flow, pull original discount rate and recreate base cash_flow
            discount_rate = analysis.dRateReal if analysis.outputRealBool else analysis.dRateNom
            for _id, bcn in enumerate(base_input.bcnObjects):
                cash_flow.pop(bcn)
                cash_flow[bcn] = cash_flows(bcn, analysis.studyPeriod, discount_rate, timestep_comp)

        iteration += 1

    # Return list of SensitivitySummaries, with altered values
    return res

def runCF(base_input, timestep_comp, dependencies=None):
    analysis = base_input.analysisObject
    discount_rate = analysis.dRateReal if analysis.outputRealBool else analysis.dRateNom

    return {bcn: cash_flows(bcn, analysis.studyPeriod, discount_rate, timestep_comp) for bcn in base_input.bcnObjects}


def present_value(v: CostType, d: CostType, t: CostType, timestep_comp: str) -> CostType:
    """
    Converts the given value to a present value with the given discount and time values.

    :param timestep_comp:
    :param v: The value to discount.
    :param d: The discount rate to apply.
    :param t: The amount of time to discount.
    :return: The value discounted to its present value.
    """
    # If timestepComp is "MidYear":
    if timestep_comp == "MidYear" and t != 0:
        return v * (1 / (1 + d)) ** (t - CostType("0.5"))
    elif timestep_comp == "MidYear" and t == 0:
        return v
    # If timestepComp is EndOfYear:
    elif timestep_comp == "EndOfYear":
        return v * (1 / (1 + d)) ** t
    # If timestepComp is Continuous:
    elif timestep_comp == "Continuous":
        return v * Decimal(1 / math.exp(d * t))


def discount_values(rate: CostType, value_list: List[CostType], timestep_comp: str):
    """
    Discounts the given list of values to their present values with the given rate.

    :param timestep_comp:
    :param rate: The discount rate.
    :param value_list: The list of values to discount.
    :return: A list of discounted values.
    """
    return list(map(lambda x: present_value(x[1], rate, CostType(x[0]), timestep_comp), enumerate(value_list)))


def calculate_values(bcn: Bcn, study_period: int, quantities: List[CostType]) -> Generator[CostType, None, None]:
    """
    Calculates the non-discounted values for over the study period from the given quantities.

    :param bcn: The BCN to calculate values for.
    :param study_period: The study period the analysis is over.
    :param quantities: The list of quantities.
    :return: A list of non-discounted values in the correct position in a study period length array.
    """
    recur_var_value = get_recur_generator(bcn)
    return generator_base(
        bcn,
        study_period,
        lambda i: quantities[i] * bcn.valuePerQ * next(recur_var_value)
    )


def get_recur_generator(bcn: Bcn) -> Generator[CostType, None, None]:
    """
    Returns the correct generator for the given BCN.

    :param bcn: The BCN to get the recur generator for.
    :return: Either a single value, year by year, or var value generator.
    """
    if bcn.is_single_recur_value:
        return single_value(bcn)

    if bcn.recurVarRate == VAR_RATE_OPTIONS[1]:
        return year_by_year(bcn.initialOcc, bcn.recurEndDate, bcn.recurVarValue)

    return var_value(bcn.recurEndDate, bcn.initialOcc, bcn.recurInterval, bcn.recurVarValue)


def year_by_year(initial: int, recur_end_date: int, var_value_list) -> Generator[CostType, None, None]:
    """
    A generator which calculates var values year by year.

    :param initial: The initial occurrence of the BCN.
    :param recur_end_date: The end date of the BCN.
    :param var_value_list: The list of variation in the BCN.
    :return: A generator returning the next var value.
    """
    for i in range(initial, recur_end_date + 1):
        yield var_value_list[i]


def single_value(bcn: Bcn) -> Generator[CostType, None, None]:
    """
    A generator which calculates the var values for this BCN if they are not compounding.

    :return: A generator returning the next var value.
    """
    for i in range(0, bcn.recurEndDate + 1):
        if i >= bcn.initialOcc and (i - bcn.initialOcc) % bcn.recurInterval == 0:
            yield (1 + bcn.recurVarValue[i]) ** i


def var_value(recur_end_date: int, initial: int, interval: int, var_value_list) -> Generator[CostType, None, None]:
    """
    A generator which calculates the var values for this BCN if they should be compounding.

    :param recur_end_date: The end date of the BCN recurrence.
    :param initial: The start of the BCN recurrence
    :param interval: The timestep interval of the BCN.
    :param var_value_list: The var value list of the BCN.
    :return: A generator returning the next var value.
    """
    result = 1

    for i in range(0, recur_end_date + 1):
        if result == 0 and var_value_list[i] != 0:
            result = 1

        result = result * (1 + var_value_list[i])
        # -------------------------
        if i == 0 and initial == 0:
            yield result
        elif i == 1 and initial == 0 and interval != 1:
            pass
        elif i >= initial and (i - max(1, initial)) % interval == 0:
            yield result
        # -------------------------


def quantity_generator(bcn: Bcn):
    """
    Returns the quantity var value generator for the given BCN.

    :param bcn: The BCN to get the quantity var value generator for.
    :return: A generator with year by year or var values for quantity.
    """
    if bcn.quantVarRate == VAR_RATE_OPTIONS[1]:
        return year_by_year(bcn.initialOcc, bcn.recurEndDate, bcn.quantVarValue)

    return var_value(bcn.recurEndDate, bcn.initialOcc, bcn.recurInterval, bcn.quantVarValue)


def calculate_quantities(bcn: Bcn, study_period: int) -> Generator[CostType, None, None]:
    """
    Calculates the quantities over the study period.

    :param bcn: The BCN to calculate quantities for.
    :param study_period: The study period the analysis is over.
    :return: A list of quantities at the correct position in a study period length array.
    """
    quantity_var_value = quantity_generator(bcn)
    return generator_base(bcn, study_period, lambda _: bcn.quant * next(quantity_var_value))


def generator_base(bcn: Bcn, study_period, calculation) -> Generator[CostType, None, None]:
    """
    Creates a generator which performs the given calculation in the correct time slots or else returns 0.

    :param bcn: The BCN to make a generator base for.
    :param study_period: The length of the study period, the generator will produce a list of this value plus one.
    :param calculation: A lambda which takes the current index and returns a CostType.
    :return: A generator which returns CostType objects.
    """
    for i in range(0, study_period + 1):
        if i == 0 and bcn.initialOcc == 0:
            yield calculation(i)
        elif i == 1 and bcn.initialOcc == 0 and bcn.recurInterval != 1:
            yield CostType("0")
        elif i < bcn.initialOcc or (i - max(1, bcn.initialOcc)) % bcn.recurInterval or i > bcn.recurEndDate:
            yield CostType("0")
        else:
            yield calculation(i)


def remaining_life(bcn: Bcn, study_period: int):
    """
    Calculate the remaining life of this bcn. This can change depending on if it is recurring, the properties
    of the recursion, or if it is a single cost.

    :param bcn: The BCN to calculate remaining life for.
    :param study_period: The length of the study period.
    :return: The remaining life of the bcn.
    """

    first_year = max(1, bcn.initialOcc)

    def last_interval():
        return math.floor((study_period - first_year) / bcn.recurInterval) * bcn.recurInterval + first_year

    def end_date_within_period():
        return not bcn.is_recur_end_date_none and bcn.recurEndDate <= study_period

    def lifetime_within_period():
        if bcn.recurBool and bcn.is_recur_end_date_none:
            return False

        return study_period >= bcn.bcnLife + last_interval() - 1

    def one_time_within_period():
        return not bcn.recurBool and study_period > first_year + bcn.bcnLife - 1

    if end_date_within_period() or lifetime_within_period() or bcn.initialOcc > study_period or one_time_within_period():
        return 0
    elif bcn.recurBool:
        return bcn.bcnLife - (study_period - last_interval()) - 1
    else:
        residual_life = bcn.bcnLife - study_period
        if bcn.initialOcc != 0:
            residual_life += first_year - 1
        return residual_life


def residual_value(bcn: Bcn, study_period: int, values: Sequence[CostType]) -> list[CostType]:
    """
    Calculate the residual value of the bcn and place the resulting value in the give values array.

    :param bcn: The BCN to calculate residual value for.
    :param study_period: The length of the study period.
    :param values: The list of values to place the result in to.
    :return: The list of values with the new residual value added.
    """
    result = [CostType(0)] * len(values) if bcn.rvOnly else list(values)
    remaining = remaining_life(bcn, study_period)

    # If the initial occurrence is greater than study period, return result
    if bcn.initialOcc > study_period:
        return [CostType(0)] * len(values)

    result[study_period] += CostType(-remaining / bcn.bcnLife) * values[bcn.initialOcc]

    return result


def cash_flows(bcn: Bcn, study_period: int, rate: CostType, timestep_comp: str) -> FlowType:
    """
    Discounts this BCN to its present value and returns final and intermediate values.

    :param timestep_comp:
    :param bcn: The BCN to create cash flows for.
    :param study_period: The range that this BCN is over.
    :param rate:  The discount rate.
    :return: A tuple of discounted values over the study period.
    """
    if not isinstance(rate, CostType):
        rate = CostType(rate)

    quantities = list(calculate_quantities(bcn, study_period))
    values = list(calculate_values(bcn, study_period, quantities))

    if bcn.rvBool:
        values = residual_value(bcn, study_period, values)

    discounted_list = discount_values(rate, values, timestep_comp)

    return quantities, values, discounted_list


def analyze(user_input: Input):
    """
    Main task that runs analysis.

    :param user_input: The input object the user provides.
    :return: The json output created by the analysis.
    """

    module_graph = ModuleGraph()
    cache = {}

    clean_module_list = deepcopy(user_input.analysisObject.objToReport)
    if "IRRSummary" in clean_module_list:
        clean_module_list.remove("IRRSummary")

    # EdgesSummary should be last item in clean_module_list
    if "EdgesSummary" in clean_module_list:
        user_input.edgesObject.override_input(user_input)

    result = {name: module_graph.run(name, user_input, cache) for name in clean_module_list}

    for x, y in result.items():
        for i in y:
            print(i)

    return OutputSerializer(Output(**result)).data
