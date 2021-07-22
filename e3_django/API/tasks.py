import logging
from typing import Union

from celery import shared_task

from API import registry
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

    flows = {bcn: bcn.cashFlows(analysis.studyPeriod, analysis.dRateReal) for bcn in user_input.bcnObjects}

    # Generate required cash flows
    required = {}
    for bcn in user_input.bcnObjects:
        for alt in bcn.altID:
            required[alt] = required.get(alt, RequiredCashFlow(alt, analysis.studyPeriod)).add(bcn, flows[bcn])

    # Generate empty cash flows for all tags
    # FIXME: Maybe have all tags defined in one place so we don't have to search through all bcns for them.
    optionals = {}
    for bcn in user_input.bcnObjects:
        for tag in bcn.bcnTag:
            if not bcn.bcnTag:
                continue

            for alt in user_input.alternativeObjects:
                key = (alt.altID, tag)

                if key in optionals:
                    continue

                optionals[key] = OptionalCashFlow(alt.altID, tag, bcn.quantUnit, user_input.analysisObject.studyPeriod)

    # Calculate optional cash flows
    for bcn in user_input.bcnObjects:
        for tag in bcn.bcnTag:
            for alt in bcn.altID:
                key = (alt, tag)
                optionals[key].add(bcn, flows[bcn])

    return OutputSerializer(Output(list(required.values()), optCashFlowObjects=list(optionals.values()))).data


@shared_task
def runModule(outputOption: Union[str, list[str]], userInput):
    return registry.moduleFunctions[outputOption](userInput)
