from rest_framework.fields import ListField
from API.registry import E3ModuleConfig

from API.serializers.SensitivitySerializer import SensitivitySerializer
from compute.cashflow.apps import cash_flows
from compute.objects import SensitivitySummary
from compute.optional.apps import calculate_tag_flows
from compute.required.apps import calculate_required_flows
from compute.measures.apps import calculate_alternative_summaries
from compute.serializers import SensitivitySummarySerializer
import numpy


class SensitivityConfig(E3ModuleConfig):
    """
    This module calculates the sensitivity objects from BCN objects.
    """

    name = "compute.sensitivity"
    verbose_name = 'E3 Sensitivity Generator'
    depends_on = ["internal:cash-flows"]
    output = "SensitivitySummary"
    serializer = ListField(child=SensitivitySummarySerializer(), required=False)

    def run(self, base_input, dependencies=None):
        """
        Purpose: Re-runs Analysis with updated values, stores output, returns list
        of sensitivity summaries.
        """

        # Generate each Sensitivity object with the base_input, in a Loop:
        res = []
        for _id, sensitivity_object in enumerate(base_input.sensitivityObjects):
            # Collect information from analysis object and pull base calculation cash flows
            timestep_comp = base_input.analysisObject.timestepComp
            analysis = base_input.analysisObject
            study_period = analysis.studyPeriod
            cash_flow = dependencies["internal:cash-flows"]
            bcn_objects = base_input.bcnObjects

            # Generate new cash flow with updated results. Also collect values needed for new calculations
            cash_flow, global_var, new_bcn, bcn_obj, discount_rate = make_cash_flows(sensitivity_object, analysis,
                                                                                     bcn_objects, cash_flow, base_input,
                                                                                     timestep_comp)

            # Create new summaries
            new_optional_summary, new_required_summary = make_new_summaries(cash_flow, cash_flow.keys(), study_period,
                                                                            base_input)

            # Calculate updated MeasureSummary
            new_measure_summary = list(calculate_alternative_summaries(analysis,
                                       new_required_summary, new_optional_summary,
                                       base_input.alternativeObjects))

            # Generate sensitivitySummary
            sensSumm = SensitivitySummary(global_var, sensitivity_object.bcnObj, sensitivity_object.varName,
                                          sensitivity_object.diffType, sensitivity_object.diffValue,
                                          numpy.sign(sensitivity_object.diffValue), new_measure_summary)

            # Add sensitivity summary to collection of all objects of the same kind
            res.append(sensSumm)

            # Clean up alterations
            cash_flow = reset_cash_flow(sensitivity_object, cash_flow, analysis, bcn_objects, discount_rate,
                                        timestep_comp, new_bcn, bcn_obj)

        # Return list of SensitivitySummaries, with altered values
        return res


def make_cash_flows(sensitivity_object, analysis_object, bcn_objects, cash_flow, base_input, timestep_comp):
    """
    Code to generate cash flows adjusted according to the sensitivity object

    :param sensitivity_object: The sensitivity object being examined
    :param analysis_object: The analysis object
    :param bcn_objects: List of all BCN objects
    :param cash_flow: The cash flows from the base analysis
    :param base_input: User input data
    :param timestep_comp: The compounding type for the analysis
    :return: Updated cash flow, the global variable boolean, the new bcn object and the discount rate
    """
    if sensitivity_object.globalVarBool is False or not sensitivity_object.globalVarBool:
        # Get discount rate and generate updated BCN object for altered variable
        discount_rate = analysis_object.dRateReal if analysis_object.outputRealBool else analysis_object.dRateNom
        new_bcn = sensitivity_object.calculateOutput(base_input)
        # Pull BCN object based on bcnID defined by sensitivity object
        for _id, bcn in enumerate(bcn_objects):
            if bcn.bcnID == sensitivity_object.bcnID:
                bcn_obj = bcn
                break
        # Remove unaltered cash flow for BCN object from cash_flow
        cash_flow.pop(bcn_obj)
        # Update cash flows with altered BCN object flows
        cash_flow[new_bcn] = cash_flows(new_bcn, analysis_object.studyPeriod, discount_rate, timestep_comp)
        # Set globalVar to false (used as output in sensitivitySummary object)
        global_var = False
    else:
        # Get new discount rate
        discount_rate = sensitivity_object.calculateOutput(base_input, analysis_object)
        new_bcn = None
        bcn_obj = None
        # Recreate cash flows for all BCNs and populate the empty cash_flow object
        for _id, bcn in enumerate(bcn_objects):
            cash_flow.pop(bcn)
            cash_flow[bcn] = cash_flows(bcn, analysis_object.studyPeriod, discount_rate, timestep_comp)
        # Set globalVar to true (used as output in sensitivitySummary object)
        global_var = True

    return cash_flow, global_var, new_bcn, bcn_obj, discount_rate


def make_new_summaries(cash_flow, cash_flow_keys, study_period, base_input):
    """
    Generates new summaries for the sensitivity analysis

    :param cash_flow: The adjusted cash flows
    :param cash_flow_keys: Dictionary keys to pull cash flow values
    :param study_period: The study period for the analysis
    :param base_input:  User input data
    :return: The optional and required summaries for the sensitivity object
    """

    # Calculate updated OptionalSummary
    new_optional_summary = calculate_tag_flows(cash_flow, base_input, cash_flow_keys)

    # Calculate updated FlowSummary
    new_required_summary = calculate_required_flows(cash_flow_keys, study_period, cash_flow)

    return new_optional_summary, new_required_summary


def reset_cash_flow(sensitivity_object, cash_flow, analysis_object, bcn_objects, discount_rate, timestep_comp,
                    new_bcn=None, bcn_obj=None):
    """
    Reverts sensitivity changes to the base anlaysis values

    :param sensitivity_object: The sensitivity object being examined
    :param cash_flow: The adjusted cash flow
    :param analysis_object: The analysis object
    :param bcn_objects: List of all BCN objects
    :param discount_rate: The discount rate for the analysis
    :param timestep_comp: The compounding type for the analysis
    :param new_bcn: The BCN updated for the sensitivity adjustment (if adjustment is not global)
    :param bcn_obj: The bcn object that was adjusted (if adjustment is not global)
    :return: The cash flow reverted to pre-sensitivity values
    """

    if sensitivity_object.globalVarBool is False or not sensitivity_object.globalVarBool:
        # Remove updated BCN, recalculate original BCN and add back to cash_flow
        cash_flow.pop(new_bcn)
        cash_flow[bcn_obj] = cash_flows(bcn_obj, analysis_object.studyPeriod, discount_rate, timestep_comp)
    else:
        # Rebuild original cash flow
        discount_rate = analysis_object.dRateReal if analysis_object.outputRealBool else analysis_object.dRateNom
        for _id, bcn in enumerate(bcn_objects):
            cash_flow.pop(bcn)
            cash_flow[bcn] = cash_flows(bcn, analysis_object.studyPeriod, discount_rate, timestep_comp)

    return cash_flow
