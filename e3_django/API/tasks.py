from celery import shared_task

from API.objects import Input, Output
from API.registry import ModuleGraph
from API.serializers.OutputSerializer import OutputSerializer
from copy import deepcopy


@shared_task
def analyze(user_input: Input):
    """
    Main task that runs analysis.

    :param user_input: The input object the user provides.
    :return: The json output created by the analysis.
    """
    module_graph = ModuleGraph()
    cache = {}
    
    clean_module_list = deepcopy(user_input.analysisObject.objToReport)
    # EdgesSummary should be last item in clean_module_list
    if "EdgesSummary" in clean_module_list:
        user_input.edgesObject.override_input(user_input)

    if "IRRSummary" in clean_module_list:
        clean_module_list.remove("IRRSummary")

    result = {name: module_graph.run(name, user_input, cache) for name in clean_module_list}

    for x, y in result.items():
        for i in y:
            print(i)

    return OutputSerializer(Output(**result)).data
