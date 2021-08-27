from typing import Union

from celery import shared_task

from API import registry
from API.objects import AlternativeSummary
from API.objects.CashFlow import RequiredCashFlow, OptionalCashFlow
from API.objects.Input import Input
from API.objects.Output import Output
from API.serializers.OutputSerializer import OutputSerializer


@shared_task
def analyze(user_input: Input):
    """
    Main task that runs analysis.

    :param user_input: The input object the user provides.
    :return: The json output created by the analysis.
    """

    analysis = user_input.analysisObject

    flows = {bcn: bcn.cash_flows(analysis.studyPeriod, analysis.dRateReal) for bcn in user_input.bcnObjects}

    required = calculate_required_flows(flows, user_input)
    optionals = calculate_tag_flows(flows, user_input)

    # Calculate Measures
    summaries = calculate_alternative_summaries(required, optionals)

    return OutputSerializer(Output(summaries, required, optionals)).data

def calculate_alternative_summaries(required_flows: list[RequiredCashFlow], optional_flows: list[OptionalCashFlow]) \
        -> list[AlternativeSummary]:
    def create_filter(alt_id):
        def wrapped(flow):
            return flow.aldID == alt_id

        return wrapped

    for required in required_flows:
        optionals = filter(create_filter(required.altID), optional_flows)

    return []

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
            if not bcn.bcnTag:
                continue

            for alt in user_input.alternativeObjects:
                key = (alt.altID, tag)

                if key in result:
                    continue

                result[key] = OptionalCashFlow(alt.altID, tag, bcn.quantUnit, user_input.analysisObject.studyPeriod)

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
            for alt in bcn.altID:
                key = (alt, tag)
                optionals[key].add(bcn, flows[bcn])

    return list(optionals.values())


@shared_task
def run_module(output_option: Union[str, list[str]], user_input):
    return registry.moduleFunctions[output_option](user_input)
