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
        required = {}
        for bcn in base_input.bcnObjects:
            for alt in bcn.altID:
                required[alt] = required \
                    .get(alt, RequiredCashFlow(alt, base_input.analysisObject.studyPeriod)) \
                    .add(bcn, dependencies["internal:cash-flows"][bcn])

        return list(required.values())
