from rest_framework.fields import ListField

from API.registry import E3ModuleConfig
from compute.objects import RequiredCashFlow
from compute.serializers import RequiredCashFlowSerializer


class RequiredCashFlowConfig(E3ModuleConfig):
    """
    This module calculates required cash flows from BCN cash flows.
    """

    name = "compute.required"
    verbose_name = 'E3 Required Cash Flow Object'

    depends_on = ["internal:cash-flows"]
    output = "FlowSummary"
    serializer = ListField(child=RequiredCashFlowSerializer(), required=False)

    def run(self, base_input, dependencies=None):
        return calculate_required_flows(base_input.bcnObjects, base_input.analysisObject.studyPeriod, \
            dependencies["internal:cash-flows"])


def calculate_required_flows(bcnObjects, studyPeriod, cashFlows):
    required = {}
    for bcn in bcnObjects:
        for alt in bcn.altID:
            required[alt] = required \
                .get(alt, RequiredCashFlow(alt, studyPeriod)) \
                .add(bcn, cashFlows[bcn])

    return list(required.values())