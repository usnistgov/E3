import logging
from decimal import Decimal
from typing import Union, Iterable

from celery import shared_task
from rest_framework.fields import DecimalField
from rest_framework.serializers import Serializer

from API import registry
from API.objects import AlternativeSummary, Analysis, Alternative
from API.objects.CashFlow import RequiredCashFlow, OptionalCashFlow
from API.objects.Input import Input
from API.objects.Output import Output
from API.serializers.OutputSerializer import OutputSerializer
from API.serializers.fields import InfinityDecimalField


@shared_task
def analyze(user_input: Input):
    """
    Main task that runs analysis.

    :param user_input: The input object the user provides.
    :return: The json output created by the analysis.
    """

    analysis = user_input.analysisObject

    discount_rate = analysis.dRateReal if analysis.outputRealBool else analysis.dRateNom

    flows = {bcn: bcn.cash_flows(analysis.studyPeriod, discount_rate) for bcn in user_input.bcnObjects}

    required = calculate_required_flows(flows, user_input)
    optionals = calculate_tag_flows(flows, user_input)

    # Calculate Measures
    summaries = list(
        calculate_alternative_summaries(user_input.analysisObject, required, optionals, user_input.alternativeObjects)
    )

    return OutputSerializer(Output(summaries, required, optionals)).data


def calculate_alternative_summaries(analysis: Analysis, required_flows: Iterable[RequiredCashFlow],
                                    optional_flows: Iterable[OptionalCashFlow], alternatives: Iterable[Alternative]) \
        -> Iterable[AlternativeSummary]:
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


def calculate_required_flows(flows, user_input):
    # Generate required cash flows
    required = {}
    for bcn in user_input.bcnObjects:
        for alt in bcn.altID:
            required[alt] = required \
                .get(alt, RequiredCashFlow(alt, user_input.analysisObject.studyPeriod)) \
                .add(bcn, flows[bcn])

    return list(required.values())


def create_empty_tag_flows(user_input):
    """
    Generate empty cash flows for every tag in the bcn object set.

    :param user_input: The input object.
    :return: A dict of (alt, tag) to empty cash flows for every tag for every bcn.
    """
    # FIXME: Maybe have all tags defined in one place so we don't have to search through all bcns for them.
    result = {}

    for bcn in user_input.bcnObjects:
        for tag in bcn.bcnTag:
            if not tag:
                continue

            for alt_id in bcn.altID:
                key = (alt_id, tag)

                if key in result:
                    continue

                result[key] = OptionalCashFlow(alt_id, tag, bcn.quantUnit, user_input.analysisObject.studyPeriod)

    return result


def calculate_tag_flows(flows, user_input):
    """
    Calculate cash flows for all tags in bcn set.

    :param flows: The cash flows calculated from the bcn objects.
    :param user_input: The input object.
    :return: A list of cash flows for all tags. Some flows may be empty for some alternatives.
    """
    optionals = create_empty_tag_flows(user_input)

    for bcn in user_input.bcnObjects:
        for tag in bcn.bcnTag:
            if not tag:
                continue

            for alt in bcn.altID:
                key = (alt, tag)
                optionals[key].add(bcn, flows[bcn])

    return list(optionals.values())


@shared_task
def run_module(output_option: Union[str, list[str]], user_input):
    return registry.moduleFunctions[output_option](user_input)
