from celery import shared_task

from API.objects.Input import Input
from API.objects.Output import Output
from API.registry import ModuleGraph
from API.serializers.OutputSerializer import OutputSerializer


@shared_task
def analyze(user_input: Input):
    """
    Main task that runs analysis.

    :param user_input: The input object the user provides.
    :return: The json output created by the analysis.
    """
    cache = {}
    result = {obj: ModuleGraph().run(obj, user_input, cache) for obj in user_input.analysisObject.objToReport}

    return OutputSerializer(Output(**result)).data
