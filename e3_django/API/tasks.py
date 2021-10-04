from typing import Union

from celery import shared_task

from API import registry
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
    registry.reset()

    output_objects = {
        name: registry.moduleFunctions[name](user_input) for name in user_input.analysisObject.objToReport
    }

    return OutputSerializer(Output(**output_objects)).data


@shared_task
def run_module(output_option: Union[str, list[str]], user_input):
    return registry.moduleFunctions[output_option](user_input)
