import operator
import pprint

from API.serializers import CostType


def elementwiseAdd(x, y):
    return list(map(operator.add, x, y))


class CashFlow:
    def add(self, bcn, flow):
        pass

    def print(self):
        pp = pprint.PrettyPrinter(indent=4, depth=2, compact=True, width=400)
        pp.pprint(self.__dict__)


class RequiredCashFlow(CashFlow):
    def __init__(self, alt, studyPeriod):
        default = [CostType(0)] * (studyPeriod + 1)

        self.altID = alt

        self.totCostNonDisc = default
        self.totCostDisc = default
        self.totBenefitsNonDisc = default
        self.totBenefitsDisc = default

        self.totCostsNonDiscInv = default
        self.totCostsDiscInv = default
        self.totBenefitsNonDiscInv = default
        self.totBenefitsDiscInv = default

        self.totCostNonDiscNonInv = default
        self.totCostDiscNonInv = default
        self.totBenefitsNonDiscNonInv = default
        self.totBenefitsDiscNonInv = default

        self.totCostDir = default
        self.totCostDirDisc = default
        self.totBenefitsDir = default
        self.totBenefitsDirDisc = default

        self.totCostInd = default
        self.totCostIndDisc = default
        self.totBenefitsInd = default
        self.totBenefitsIndDisc = default

        self.totCostExt = default
        self.totCostExtDisc = default
        self.totBenefitsExt = default
        self.totBenefitsExtDisc = default

    def add(self, bcn, flow):
        if bcn.bcnType == "Cost":
            self.totCostNonDisc = elementwiseAdd(self.totCostNonDisc, flow[1])
            self.totCostDisc = elementwiseAdd(self.totCostDisc, flow[2])
        elif bcn.bcnType == "Benefits":
            self.totBenefitsNonDisc = elementwiseAdd(self.totBenefitsNonDisc, flow[1])
            self.totBenefitsDisc = elementwiseAdd(self.totBenefitsDisc, flow[2])

        if bcn.bcnInvestBool:
            if bcn.bcnType == "Cost":
                self.totCostsNonDiscInv = elementwiseAdd(self.totCostsNonDiscInv, flow[1])
                self.totCostsDiscInv = elementwiseAdd(self.totCostsDiscInv, flow[2])
            elif bcn.bcnType == "Benefits":
                self.totBenefitsNonDiscInv = elementwiseAdd(self.totBenefitsNonDiscInv, flow[1])
                self.totBenefitsDiscInv = elementwiseAdd(self.totBenefitsDiscInv, flow[2])
        else:
            if bcn.bcnType == "Cost":
                self.totCostNonDiscNonInv = elementwiseAdd(self.totCostNonDiscNonInv, flow[1])
                self.totCostDiscNonInv = elementwiseAdd(self.totCostDiscNonInv, flow[2])
            elif bcn.bcnType == "Benefits":
                self.totBenefitsNonDiscNonInv = elementwiseAdd(self.totBenefitsNonDiscNonInv, flow[1])
                self.totBenefitsDiscNonInv = elementwiseAdd(self.totBenefitsDiscNonInv, flow[2])

        if bcn.bcnSubType == "Direct":
            if bcn.bcnType == "Cost":
                self.totCostDir = elementwiseAdd(self.totCostDir, flow[1])
                self.totCostDirDisc = elementwiseAdd(self.totCostDirDisc, flow[2])
            elif bcn.bcnType == "Benefits":
                self.totBenefitsDir = elementwiseAdd(self.totBenefitsDir, flow[1])
                self.totBenefitsDirDisc = elementwiseAdd(self.totBenefitsDirDisc, flow[2])
        elif bcn.bcnSubType == "Indirect":
            if bcn.bcnType == "Cost":
                self.totCostInd = elementwiseAdd(self.totCostInd, flow[1])
                self.totCostIndDisc = elementwiseAdd(self.totCostIndDisc, flow[2])
            elif bcn.bcnType == "Benefits":
                self.totBenefitsInd = elementwiseAdd(self.totBenefitsInd, flow[1])
                self.totBenefitsIndDisc = elementwiseAdd(self.totBenefitsIndDisc, flow[2])
        else:
            if bcn.bcnType == "Cost":
                self.totCostExt = elementwiseAdd(self.totCostExt, flow[1])
                self.totCostExtDisc = elementwiseAdd(self.totCostExtDisc, flow[2])
            elif bcn.bcnType == "Benefits":
                self.totBenefitsExt = elementwiseAdd(self.totBenefitsExt, flow[1])
                self.totBenefitsExtDisc = elementwiseAdd(self.totBenefitsExtDisc, flow[2])

        return self


class OptionalCashFlow(CashFlow):
    def __init__(self, altID, tag, units, studyPeriod):
        default = [CostType(0)] * (studyPeriod + 1)

        self.altID = altID
        self.tag = tag

        self.totTagFlowDisc = default
        self.totTagQ = default
        self.quantUnits = units

    def add(self, bcn, flow):
        self.totTagFlowDisc = elementwiseAdd(self.totTagFlowDisc, flow[2])
        self.totTagQ = elementwiseAdd(self.totTagFlowDisc, flow[0])

        return self
