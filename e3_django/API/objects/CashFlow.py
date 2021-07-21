import logging
import pprint
from functools import reduce
from typing import Callable, Any

from API.serializers import CostType


class CashFlow:
    def __init__(self, altID, bcnCashFlows, studyPeriod):
        logging.info(bcnCashFlows)

        def reduceFlow(predicate: Callable[[Any], bool] = lambda _: True, discounted: bool = False):
            return list(reduce(
                lambda x, y: map(CostType.__add__, x, y),
                [x[1][2 if discounted else 1] for x in bcnCashFlows.items() if predicate(x)],
                [CostType(0)] * (studyPeriod + 1)
            ))

        self.altID = altID

        self.totCostNonDisc = reduceFlow()
        self.totCostDisc = reduceFlow(discounted=True)
        self.totBenefitsNonDisc = reduceFlow()
        self.totBenefitsDisc = reduceFlow(discounted=True)

        def InvestPredicate(x):
            return x[0].bcnInvestBool

        self.totCostsNonDiscInv = reduceFlow(InvestPredicate)
        self.totCostsDiscInv = reduceFlow(InvestPredicate, True)
        self.totBenefitsNonDiscInv = reduceFlow(InvestPredicate)
        self.totBenefitsDiscInv = reduceFlow(InvestPredicate, True)

        def NonInvestPredicate(x):
            return not x[0].bcnInvestBool

        self.totCostNonDiscNonInv = reduceFlow(NonInvestPredicate)
        self.totCostDiscNonInv = reduceFlow(NonInvestPredicate, True)
        self.totBenefitsNonDiscNonInv = reduceFlow(NonInvestPredicate)
        self.totBenefitsDiscNonInv = reduceFlow(NonInvestPredicate, True)

        def DirectPredicate(x):
            return x[0].bcnSubType == "Direct"

        self.totCostDir = reduceFlow(DirectPredicate)
        self.totCostDirDisc = reduceFlow(DirectPredicate, True)
        self.totBenefitsDir = reduceFlow(DirectPredicate)
        self.totBenefitsDirDisc = reduceFlow(DirectPredicate, True)

        def IndirectPredicate(x):
            return x[0].bcnSubType == "Indirect"

        self.totCostInd = reduceFlow(IndirectPredicate)
        self.totCostIndDisc = reduceFlow(IndirectPredicate, True)
        self.totBenefitsInd = reduceFlow(IndirectPredicate)
        self.totBenefitsIndDisc = reduceFlow(IndirectPredicate, True)

        def NeitherPredicate(x):
            return x[0].bcnSubType != "Indirect" and x[0].bcnSubType != "Direct"

        self.totCostExt = reduceFlow(NeitherPredicate)
        self.totCostExtDisc = reduceFlow(NeitherPredicate, True)
        self.totBenefitsExt = reduceFlow(NeitherPredicate)
        self.totBenefitsExtDisc = reduceFlow(NeitherPredicate, True)

    def print(self):
        pp = pprint.PrettyPrinter(indent=4, depth=2, compact=True, width=400)
        pp.pprint(self.__dict__)
