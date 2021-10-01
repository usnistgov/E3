import logging

from API.registry import E3AppConfig


class CashFlowConfig(E3AppConfig):
    name = "compute.cashflow"
    verbose_name = 'E3 Cash Flow Generator'

    output = "internal:cash-flows"

    def analyze(self, base_input, steps=None):
        analysis = base_input.analysisObject
        discount_rate = analysis.dRateReal if analysis.outputRealBool else analysis.dRateNom

        return {bcn: bcn.cash_flows(analysis.studyPeriod, discount_rate) for bcn in base_input.bcnObjects}