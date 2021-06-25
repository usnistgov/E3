from typing import Union

from celery import shared_task

from API import registry


@shared_task
def analyze(input):
    """
    Main task that runs analysis.

    :param input: The json input the user provides.
    :return: The json output created by the analysis.
    """

    return {}


@shared_task
def runModule(outputOption: Union[str, list[str]], userInput):
    return registry.moduleFunctions[outputOption](userInput)
