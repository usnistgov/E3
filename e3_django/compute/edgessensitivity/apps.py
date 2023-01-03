import math
import operator
from decimal import Decimal
from typing import Iterable

import numpy
from API.registry import E3ModuleConfig
from rest_framework.fields import ListField
from compute.objects import EdgesSensitivitySummary
from compute.serializers import EdgesSensitivitySummarySerializer
from compute.sensitivity.apps import make_cash_flows, make_new_summaries, reset_cash_flow
from compute.measures.apps import calculate_alternative_summaries
from compute.edges.apps import calculate_edges_summary


from compute.objects import RequiredCashFlow, OptionalCashFlow, EdgesSummary, AlternativeSummary, SensitivitySummary
from compute.objects.AlternativeSummary import bcr, irrMeas
from API.objects import Analysis, Alternative


class EdgesSensitivityConfig(E3ModuleConfig):
    """
    This module updates BCNs and Sensitivity objects for disaster related benefits.
    """

    name = "compute.edgessensitivity"
    verbose_name = 'E3 EDGeS Sensitivity Calculations'
    depends_on = ["internal:cash-flows"]
    output = "EdgesSensitivitySummary"
    serializer = ListField(child=EdgesSensitivitySummarySerializer(), required=False)

    def run(self, base_input, dependencies=None):
        horizon = base_input.analysisObject.studyPeriod
        for alt in base_input.alternativeObjects:
            if alt.baselineBool is True:
                baseline_id = alt.altID

        res = []
        for _id, sensitivity_object in enumerate(base_input.sensitivityObjects):
            # Collect information from analysis object and pull base calculation cash flows
            timestep_comp = base_input.analysisObject.timestepComp
            analysis = base_input.analysisObject
            study_period = analysis.studyPeriod
            cash_flow = dependencies["internal:cash-flows"]
            bcn_objects = base_input.bcnObjects

            cash_flow, global_var, new_bcn, bcn_obj, discount_rate = make_cash_flows(sensitivity_object, analysis,
                                                                                     bcn_objects, cash_flow, base_input,
                                                                                     timestep_comp)

            new_optional_summary, new_required_summary = make_new_summaries(cash_flow, cash_flow.keys(), study_period,
                                                                            base_input)

            # Calculate updated MeasureSummary
            new_measure_summary = list(calculate_alternative_summaries(analysis, new_required_summary,
                                                                       new_optional_summary,
                                                                       base_input.alternativeObjects))

            # Possible issue here with calling in lists to type Iterable
            edges_summaries = calculate_edges_summary(horizon, baseline_id, base_input.alternativeObjects,
                                                      new_required_summary, new_optional_summary, new_measure_summary)

            edgesSensSumm = EdgesSensitivitySummary(global_var, sensitivity_object.bcnObj, sensitivity_object.varName,
                                                    sensitivity_object.diffType, sensitivity_object.diffValue,
                                                    numpy.sign(sensitivity_object.diffValue), edges_summaries)

            res.append(edgesSensSumm)

            cash_flow = reset_cash_flow(sensitivity_object, cash_flow, analysis, bcn_objects, discount_rate,
                                        timestep_comp, new_bcn, bcn_obj)

        return res
