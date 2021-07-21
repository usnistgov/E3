import logging
from typing import Union

from celery import shared_task

from API import registry
from API.objects.CashFlow import CashFlow
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

    cashFlows = []
    for alt in user_input.alternativeObjects:
        logging.info(alt.altID)

        flows = {bcn: bcn.cashFlows(analysis.studyPeriod, analysis.dRateReal) for bcn in user_input.bcnObjects
                 if bcn.bcnID in alt.altBCNList}
        cashFlows.append(CashFlow(alt.altID, flows, analysis.studyPeriod))

    return OutputSerializer(Output(cashFlows)).data


@shared_task
def runModule(outputOption: Union[str, list[str]], userInput):
    return registry.moduleFunctions[outputOption](userInput)
