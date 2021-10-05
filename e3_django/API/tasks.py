from celery import shared_task

from API.objects import Input, Output
from API.registry import ModuleGraph
from API.serializers.OutputSerializer import OutputSerializer


@shared_task
def analyze(user_input: Input):
    """
    Main task that runs analysis.

    :param user_input: The input object the user provides.
    :return: The json output created by the analysis.
    """
    module_graph = ModuleGraph()
    cache = {}

    result = {name: module_graph.run(name, user_input, cache) for name in user_input.analysisObject.objToReport}

    return OutputSerializer(Output(**result)).data
