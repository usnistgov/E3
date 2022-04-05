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
        Purpose: Re-runs Analysis with updated values, store output, returns list
        of sensitivity summaries.
        """

        # Generate each Sensitivity object with the base_input, in a Loop:
        res = []
        for _id, sensitivity_object in enumerate(base_input.sensitivityObjects):
            # Collect information from analysis object
            timestep_comp = base_input.analysisObject.timestepComp
            analysis = base_input.analysisObject
            discount_rate = analysis.dRateReal if analysis.outputRealBool else analysis.dRateNom
            if analysis.outputRealBool:
                discount_rate_old = getattr(analysis, 'dRateReal')
            else:
                discount_rate_old = getattr(analysis, 'dRateNom')
            cash_flow = dependencies["internal:cash-flows"]

            if sensitivity_object.globalVarBool is False or not sensitivity_object.globalVarBool:
                # Generate updated BCN object for altered variable
                new_bcn = sensitivity_object.calculateOutput(base_input)
                # Pull correct BCN object based on bcnID defined by sensitivity object
                for _id, bcn in enumerate(base_input.bcnObjects):
                    if bcn.bcnID == sensitivity_object.bcnID:
                        bcnObj = bcn
                        break

                # Pull unaltered CashFlows and remove unaltered cash flow for BCN object
                cash_flow.pop(bcnObj)
                # Update cash flows with new BCN object
                cash_flow[new_bcn] = cash_flows(new_bcn, analysis.studyPeriod, discount_rate, timestep_comp)
                # At this point, cash_flow dictionary has an updated value for the `new_bcn`
                # Set globalVar to false (used as output in sensitivitySummary object)
                globalVar = False
            else:
                # If global we are currently only dealing with the discount rate, initialize blank cash_flow
                cash_flow = cash_flow.clear()
                # Alter discount rate (technically should be in the sensitivityObject.calculateOutput method but is
                # cleaner to include here
                if sensitivity_object.diffType == "Percent":
                    discount_rate_new = discount_rate * (1 + sensitivity_object.diffValue)
                else:
                    discount_rate_new = discount_rate + sensitivity_object.diffValue
                # Recreate cash flows for all BCNs and populate the empty cash_flow object
                for _id, bcn in enumerate(base_input.bcnObjects):
                    cash_flow[bcn] = cash_flows(bcn, analysis.studyPeriod, discount_rate_new, timestep_comp)
                # Set globalVar to true (used as output in sensitivitySummary object)
                globalVar = True

            # Calculate updated OptionalSummary
            new_optional_summary = calculate_tag_flows(cash_flow, base_input)

            # Calculate updated FlowSummary
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
                # Remove updated BCN and recalculate original BCN if globalVar == False
                cash_flow.pop(new_bcn)
                cash_flow[bcnObj] = cash_flows(bcnObj, analysis.studyPeriod,
                                               discount_rate, timestep_comp)
            else:
                # Delete entire cash_flow and return to base values
                cash_flow = cash_flow.clear()
                for _id, bcn in enumerate(base_input.bcnObjects):
                    cash_flow[bcn] = cash_flows(bcn, analysis.studyPeriod, discount_rate_old, timestep_comp)

        # Return list of SensitivitySummaries, with altered values
        return res
