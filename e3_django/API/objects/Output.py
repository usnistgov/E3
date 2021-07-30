from API.objects import OptionalCashFlow, RequiredCashFlow, AlternativeSummary


class Output:
    """
    Represents the full API output object.
    """

    def __init__(self, alternative_summaries: list[AlternativeSummary], required_cash_flows: list[RequiredCashFlow],
                 optional_cash_flows: list[OptionalCashFlow] = None):
        self.alternativeSummary = alternative_summaries
        self.reqCashFlowObjects = required_cash_flows

        if optional_cash_flows:
            self.optCashFlowObjects = optional_cash_flows
