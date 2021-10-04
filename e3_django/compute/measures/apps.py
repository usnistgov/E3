from typing import Iterable

from rest_framework.fields import ListField

from API.registry import E3AppConfig
from compute.objects import Analysis, RequiredCashFlow, OptionalCashFlow, Alternative, AlternativeSummary
from compute.serializers import AlternativeSummarySerializer


class AlternativeSummaryConfig(E3AppConfig):
    name = "compute.measures"
    verbose_name = 'E3 Measure Summary Objects'

    depends_on = ["FlowSummary", "OptionalSummary"]
    output = "MeasureSummary"
    serializer = ListField(child=AlternativeSummarySerializer(), required=False)

    def analyze(self, base_input, steps=None):
        def calculate_alternative_summaries(analysis: Analysis, required_flows: Iterable[RequiredCashFlow],
                                            optional_flows: Iterable[OptionalCashFlow],
                                            alternatives: Iterable[Alternative]) \
                -> Iterable[AlternativeSummary]:
            """
            Calculates alternative summary objects.

            :param analysis: The analysis object used for general parameters.
            :param required_flows: A list of required cash flows.
            :param optional_flows: A list of optional cash flows.
            :param alternatives: A list of alternatives.
            :return: A generator yielding alternative summaries.
            """
            baseline_alt = list(filter(lambda x: x.baselineBool, alternatives))[0]
            baseline_required_flow = list(filter(lambda x: x.altID == baseline_alt.altID, required_flows))[0]

            optionals = list(filter(lambda flow: flow.altID == baseline_alt.altID, optional_flows))

            baseline_summary = AlternativeSummary(baseline_alt.altID, analysis.reinvestRate, analysis.studyPeriod,
                                                  analysis.Marr, baseline_required_flow, optionals, None, False)

            yield baseline_summary

            for required in filter(lambda x: x.altID != baseline_alt.altID, required_flows):
                optionals = list(filter(lambda flow: flow.altID == required.altID, optional_flows))

                summary = AlternativeSummary(required.altID, analysis.reinvestRate, analysis.studyPeriod, analysis.Marr,
                                             required, optionals, baseline_summary, False)

                yield summary

        return list(calculate_alternative_summaries(base_input.analysisObject, steps[0], steps[1],
                                                    base_input.alternativeObjects))
