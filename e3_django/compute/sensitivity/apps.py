from rest_framework.fields import ListField
from API.registry import E3ModuleConfig

from API.serializers.SensitivitySerializer import SensitivitySerializer
from compute.cashflow.apps import cash_flows
from compute.objects import SensitivitySummary
from compute.optional.apps import calculate_tag_flows
from compute.required.apps import calculate_required_flows
from compute.measures.apps import calculate_alternative_summaries
import numpy


class SensitivityConfig(E3ModuleConfig):
    """
    This module calculates the sensitivity objects from BCN objects.
    """

    name = "compute.sensitivity"
    verbose_name = 'E3 Sensitivity Generator'
    depends_on = ["internal:cash-flows"]
    output = "SensitivitySummary"
    serializer = ListField(child=SensitivitySerializer(), required=False)

    def run(self, base_input, dependencies=None):
        """
        Purpose: Re-runs Analysis with updated values, store output, returns list
        of sensitivity summaries.
        """

        # Generate each Sensitivity object with the base_input, in a Loop:
        res = []
        for _id, sensitivity_object in enumerate(base_input.sensitivityObjects):
            timestep_comp = base_input.analysisObject.timestepComp
            new_bcn = sensitivity_object.calculateOutput()

            # CashFlow
            cash_flow = dependencies["internal:cash-flows"]
            cash_flow.pop(sensitivity_object.bcnObj)
            analysis = base_input.analysisObject
            discount_rate = analysis.dRateReal if analysis.outputRealBool else analysis.dRateNom

            cash_flow[new_bcn] = cash_flows(new_bcn, analysis.studyPeriod, discount_rate, timestep_comp)
            # At this point, cash_flow dictionary has an updated value for the `new_bcn`

            # Calculate updated OptionalSummary
            new_optional_summary = calculate_tag_flows(cash_flow, base_input)

            # Calculate updated FlowSummary
            new_required_summary = calculate_required_flows(cash_flow.keys(), analysis.studyPeriod, cash_flow)

            # Calculate updated MeasureSummary 
            new_measure_summary = list(calculate_alternative_summaries(analysis,
                                                                       new_required_summary, new_optional_summary,
                                                                       base_input.alternativeObjects))

            # generate sensitivitySummary
            sensSumm = SensitivitySummary(sensitivity_object.bcnObj, sensitivity_object.varName,
                                          sensitivity_object.diffType, sensitivity_object.diffVal,
                                          numpy.sign(sensitivity_object.diffVal), new_measure_summary)

            res.append(sensSumm)
            
            cash_flow.pop(new_bcn)
            cash_flow[sensitivity_object.bcnObj] = cash_flows(sensitivity_object.bcnObj, analysis.studyPeriod,
                                                              discount_rate)
        # Return list of SensitivitySummaries, with altered values
        return res
