from API.objects.CashFlow import OptionalCashFlow, RequiredCashFlow


class Output:
    def __init__(self, reqCashFlowObjects: list[RequiredCashFlow],
                 optCashFlowObjects: list[OptionalCashFlow] = None):
        self.reqCashFlowObjects = reqCashFlowObjects

        if optCashFlowObjects:
            self.optCashFlowObjects = optCashFlowObjects
