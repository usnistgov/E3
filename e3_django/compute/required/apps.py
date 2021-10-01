import logging

from API.registry import E3AppConfig
from compute.objects import RequiredCashFlow


class RequiredCashFlowConfig(E3AppConfig):
    name = "compute.required"
    verbose_name = 'E3 Required Cash Flow Object'

    depends_on = ["internal:cash-flows"]
    output = "FlowSummary"

    def analyze(self, base_input, steps=None):
        required = {}
        for bcn in base_input.bcnObjects:
            for alt in bcn.altID:
                required[alt] = required \
                    .get(alt, RequiredCashFlow(alt, base_input.analysisObject.studyPeriod)) \
                    .add(bcn, steps[0][bcn])

        return list(required.values())
