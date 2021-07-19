import pprint
from decimal import Decimal
from functools import reduce, partial

from API.serializers import CostType


class CashFlow:
    def __init__(self, altID, bcnCashFlows):
        def elementwise(operator, list1, list2):
            return list(map(operator, list1, list2))

        elementwiseAdd = partial(elementwise, CostType.__add__)

        nonDiscount = [x[1] for x in bcnCashFlows.values()]
        discount = [x[2] for x in bcnCashFlows.values()]

        self.altID = altID

        self.totCostNonDisc = reduce(elementwiseAdd, [x[1] for x in bcnCashFlows.values()], [CostType(0)] * 11)
        self.totCostDisc = reduce(elementwiseAdd, [x[2] for x in bcnCashFlows.values()], [CostType(0)] * 11)
        self.totBenefitsNonDisc = reduce(elementwiseAdd, [x[1] for x in bcnCashFlows.values()], [CostType(0)] * 11)
        self.totBenefitsDisc = reduce(elementwiseAdd, [x[2] for x in bcnCashFlows.values()], [CostType(0)] * 11)

        self.totCostsNonDiscInv = reduce(elementwiseAdd, [x[1][1] for x in bcnCashFlows.items() if x[0].bcnInvestBool], [CostType(0)] * 11)
        self.totCostsDiscInv = reduce(elementwiseAdd, [x[1][2] for x in bcnCashFlows.items() if x[0].bcnInvestBool], [CostType(0)] * 11)
        self.totBenefitsNonDiscInv = reduce(elementwiseAdd, [x[1][1] for x in bcnCashFlows.items() if x[0].bcnInvestBool], [CostType(0)] * 11)
        self.totBenefitsDiscInv = reduce(elementwiseAdd, [x[1][2] for x in bcnCashFlows.items() if x[0].bcnInvestBool], [CostType(0)] * 11)

        self.totCostNonDiscNonInv = reduce(elementwiseAdd, [x[1][1] for x in bcnCashFlows.items() if not x[0].bcnInvestBool], [CostType(0)] * 11)
        self.totCostDiscNonInv = reduce(elementwiseAdd, [x[1][2] for x in bcnCashFlows.items() if not x[0].bcnInvestBool], [CostType(0)] * 11)
        self.totBenefitsNonDiscNonInv = reduce(elementwiseAdd, [x[1][1] for x in bcnCashFlows.items() if not x[0].bcnInvestBool], [CostType(0)] * 11)
        self.totBenefitsDiscNonInv = reduce(elementwiseAdd, [x[1][2] for x in bcnCashFlows.items() if not x[0].bcnInvestBool], [CostType(0)] * 11)

        self.totCostDir = reduce(elementwiseAdd, [x[1][1] for x in bcnCashFlows.items() if x[0].bcnSubType == "Direct"], [CostType(0)] * 11)
        self.totCostDirDisc = reduce(elementwiseAdd, [x[1][2] for x in bcnCashFlows.items() if x[0].bcnSubType == "Direct"], [CostType(0)] * 11)
        self.totBenefitsDir = reduce(elementwiseAdd, [x[1][1] for x in bcnCashFlows.items() if x[0].bcnSubType == "Direct"], [CostType(0)] * 11)
        self.totBenefitsDirDisc = reduce(elementwiseAdd, [x[1][2] for x in bcnCashFlows.items() if x[0].bcnSubType == "Direct"], [CostType(0)] * 11)

        self.totCostInd = reduce(elementwiseAdd, [x[1][1] for x in bcnCashFlows.items() if x[0].bcnSubType == "Indirect"], [CostType(0)] * 11)
        self.totCostIndDisc = reduce(elementwiseAdd, [x[1][2] for x in bcnCashFlows.items() if x[0].bcnSubType == "Indirect"], [CostType(0)] * 11)
        self.totBenefitsInd = reduce(elementwiseAdd, [x[1][1] for x in bcnCashFlows.items() if x[0].bcnSubType == "Indirect"], [CostType(0)] * 11)
        self.totBenefitsIndDisc = reduce(elementwiseAdd, [x[1][2] for x in bcnCashFlows.items() if x[0].bcnSubType == "Indirect"], [CostType(0)] * 11)

        self.totCostExt = reduce(elementwiseAdd, [x[1][1] for x in bcnCashFlows.items() if x[0].bcnSubType != "Indirect" and x[0].bcnSubType != "Direct"], [CostType(0)] * 11)
        self.totCostExtDisc = reduce(elementwiseAdd, [x[1][2] for x in bcnCashFlows.items() if x[0].bcnSubType != "Indirect" and x[0].bcnSubType != "Direct"], [CostType(0)] * 11)
        self.totBenefitsExt = reduce(elementwiseAdd, [x[1][1] for x in bcnCashFlows.items() if x[0].bcnSubType != "Indirect" and x[0].bcnSubType != "Direct"], [CostType(0)] * 11)
        self.totBenefitsExtDisc = reduce(elementwiseAdd, [x[1][2] for x in bcnCashFlows.items() if x[0].bcnSubType != "Indirect" and x[0].bcnSubType != "Direct"], [CostType(0)] * 11)

    def print(self):
        pp = pprint.PrettyPrinter(indent=4, depth=2, compact=True, width=400)
        pp.pprint(self.__dict__)
