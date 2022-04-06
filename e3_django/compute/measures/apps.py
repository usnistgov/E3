from typing import Iterable

from rest_framework.fields import ListField

from API.objects import Analysis, Alternative
from API.registry import E3ModuleConfig
from compute.objects import RequiredCashFlow, OptionalCashFlow, AlternativeSummary
from compute.serializers import AlternativeSummarySerializer


class AlternativeSummaryConfig(E3ModuleConfig):
    """
    This module calculates alternative summaries based on the required and optional cash flows.
    """

    name = "compute.measures"
    verbose_name = 'E3 Measure Summary Objects'

    depends_on = ["FlowSummary", "OptionalSummary"]
    output = "MeasureSummary"
    serializer = ListField(child=AlternativeSummarySerializer(), required=False)

    def run(self, base_input, dependencies=None):
        return list(
            calculate_alternative_summaries(base_input.analysisObject, dependencies["FlowSummary"],
                                            dependencies["OptionalSummary"],
                                            base_input.alternativeObjects))


def calculate_alternative_summaries(analysis: Analysis, required_flows: Iterable[RequiredCashFlow],
                                    optional_flows: Iterable[OptionalCashFlow], alternatives: Iterable[Alternative]) \
        -> Iterable[AlternativeSummary]:
    """
    Calculates alternative summary objects.

    :param analysis: The analysis object used for general parameters.
    :param required_flows: A list of required cash flows.
    :param optional_flows: A list of optional cash flows.
    :param alternatives: A list of alternatives.
    :return: A generator yielding alternative summaries.
    """
    include_irr = "IRRSummary" in analysis.objToReport
    timestep_comp = analysis.timestepComp

    baseline_alt = list(filter(lambda x: x.baselineBool, alternatives))[0]
    baseline_required_flow = list(filter(lambda x: x.altID == baseline_alt.altID, required_flows))[0]

    optionals = list(filter(lambda flow: flow.altID == baseline_alt.altID, optional_flows))

    baseline_summary = AlternativeSummary(baseline_alt.altID, analysis.reinvestRate, analysis.studyPeriod,
                                          analysis.Marr, baseline_required_flow, optionals, timestep_comp, None,
                                          None)

    yield baseline_summary

    for required in filter(lambda x: x.altID != baseline_alt.altID, required_flows):
        optionals = list(filter(lambda flow: flow.altID == required.altID, optional_flows))

        summary = AlternativeSummary(required.altID, analysis.reinvestRate, analysis.studyPeriod, analysis.Marr,
                                     required, optionals, timestep_comp, baseline_summary, include_irr)

        yield summary
