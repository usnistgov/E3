from rest_framework.fields import ListField
from API.registry import E3ModuleConfig
from e3_django.API.objects.Sensitivity import Sensitivity
from e3_django.API.serializers.SensitivitySerializer import SensitivitySerializer
from e3_django.compute.cashflow.apps import cash_flows
from e3_django.compute.objects import SensitivitySummary
from e3_django.compute.optional.apps import calculate_tag_flows
from e3_django.compute.required.apps import calculate_required_flows
from e3_django.compute.measures.apps import calculate_alternative_summaries

class SensitivityConfig(E3ModuleConfig):
    """
    This module calculates the sensitivity objects from BCN objects.
    """

    name = "compute.sensitivity"
    verbose_name = 'E3 Sensitivity Generator'
    depends_on = ["internal:cash-flows"]
    output = "sensitivity-summary"
    serializer = ListField(child=SensitivitySerializer(), required=False)

    def run(self, base_input, dependencies=None):
        """
        Purpose: Re-runs Analysis with updated values, store output, returns list
        of sensitivity summaries.
        """

        # Generate each Sensitivity object with the base_input, in a Loop:
        res = []
        for _id, sensitivity_object in enumerate(base_input.sensitivityObjects):
            new_bcn = sensitivity_object.calculateOutput()

            # CashFlow
            cash_flow = dependencies["internal:cash-flows"]
            cash_flow.pop(sensitivity_object.bcnObj)
            analysis = base_input.analysisObject
            discount_rate = analysis.dRateReal if analysis.outputRealBool else analysis.dRateNom
            
            cash_flow[new_bcn] = cash_flows(new_bcn, analysis.studyPeriod, discount_rate)
            # At this point, cash_flow dictionary has an updated value for the `new_bcn`

            # Calculate updated OptionalSummary
            new_optional_summary = calculate_tag_flows(cash_flow, base_input)

            # Calculate updated FlowSummary
            new_required_summary = calculate_required_flows(cash_flow.keys(), \
                analysis.studyPeriod, cash_flow)

            # Calculate updated MeasureSummary 
            new_measure_summary = list(calculate_alternative_summaries(analysis, \
                new_required_summary, new_optional_summary, base_input.alternativeObjects))

            # generate sensitivitySummary
            sensitivitySummary = SensitivitySummary(
                sensitivity_id=_id,
                # Come back to this later:
                measure_summary=new_measure_summary[sensitivity_object.altID]
            )
            res.append(sensitivitySummary)
        
        # Return list of SensitivitySummaries, with altered values
        return res