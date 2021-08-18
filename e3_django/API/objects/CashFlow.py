import operator
import pprint

from API.objects import Bcn
from API.variables import CostType, FlowType


def elementwise_add(x, y):
    """
    Function that accepts two lists and adds them together element-wise.

    :param x: A list to add.
    :param y: A list to add.
    :return: A list comprised of the given lists added together element-wise.
    """
    return list(map(operator.add, x, y))


class CashFlow:
    """
    Represents a cash flow object in the API output. Functionality is added in subclasses.
    """

    def add(self, bcn: Bcn, flow: FlowType):
        """
        Method to be overridden to provide functionality for adding bcn values to this cash flow. This method should
        mutate self and return a reference to self.

        :param bcn: The BCN to add to this cash flow.
        :param flow: The flows associated with the bcn.
        :return: This class mutated with the given BCN values.
        """
        pass

    def update(self, bcn, flow):
        """To be added later for updating bcn values to this cash flow."""
        pass
    
    def updateAllFlows(self, bcn, flowsList):
        """To be added later for updating ALL bcn values to this cash flow."""
        pass

    def print(self):
        """
        Prints a representation of this cash flow. Used for debugging.
        """
        pp = pprint.PrettyPrinter(indent=4, depth=2, compact=True, width=400)
        pp.pprint(self.__dict__)


class RequiredCashFlow(CashFlow):
    """
    Represents the required cash flow objects in the user output.
    """

    def __init__(self, alt: int, study_period: int):
        default = [CostType(0)] * (study_period + 1)

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

    def add(self, bcn: Bcn, flow: FlowType):
        if bcn.bcnType == "Cost":
            self.totCostNonDisc = elementwise_add(self.totCostNonDisc, flow[1])
            self.totCostDisc = elementwise_add(self.totCostDisc, flow[2])
        elif bcn.bcnType == "Benefits":
            self.totBenefitsNonDisc = elementwise_add(self.totBenefitsNonDisc, flow[1])
            self.totBenefitsDisc = elementwise_add(self.totBenefitsDisc, flow[2])

        if bcn.bcnInvestBool:
            if bcn.bcnType == "Cost":
                self.totCostsNonDiscInv = elementwise_add(self.totCostsNonDiscInv, flow[1])
                self.totCostsDiscInv = elementwise_add(self.totCostsDiscInv, flow[2])
            elif bcn.bcnType == "Benefits":
                self.totBenefitsNonDiscInv = elementwise_add(self.totBenefitsNonDiscInv, flow[1])
                self.totBenefitsDiscInv = elementwise_add(self.totBenefitsDiscInv, flow[2])
        else:
            if bcn.bcnType == "Cost":
                self.totCostNonDiscNonInv = elementwise_add(self.totCostNonDiscNonInv, flow[1])
                self.totCostDiscNonInv = elementwise_add(self.totCostDiscNonInv, flow[2])
            elif bcn.bcnType == "Benefits":
                self.totBenefitsNonDiscNonInv = elementwise_add(self.totBenefitsNonDiscNonInv, flow[1])
                self.totBenefitsDiscNonInv = elementwise_add(self.totBenefitsDiscNonInv, flow[2])

        if bcn.bcnSubType == "Direct":
            if bcn.bcnType == "Cost":
                self.totCostDir = elementwise_add(self.totCostDir, flow[1])
                self.totCostDirDisc = elementwise_add(self.totCostDirDisc, flow[2])
            elif bcn.bcnType == "Benefits":
                self.totBenefitsDir = elementwise_add(self.totBenefitsDir, flow[1])
                self.totBenefitsDirDisc = elementwise_add(self.totBenefitsDirDisc, flow[2])
        elif bcn.bcnSubType == "Indirect":
            if bcn.bcnType == "Cost":
                self.totCostInd = elementwise_add(self.totCostInd, flow[1])
                self.totCostIndDisc = elementwise_add(self.totCostIndDisc, flow[2])
            elif bcn.bcnType == "Benefits":
                self.totBenefitsInd = elementwise_add(self.totBenefitsInd, flow[1])
                self.totBenefitsIndDisc = elementwise_add(self.totBenefitsIndDisc, flow[2])
        else:
            if bcn.bcnType == "Cost":
                self.totCostExt = elementwise_add(self.totCostExt, flow[1])
                self.totCostExtDisc = elementwise_add(self.totCostExtDisc, flow[2])
            elif bcn.bcnType == "Benefits":
                self.totBenefitsExt = elementwise_add(self.totBenefitsExt, flow[1])
                self.totBenefitsExtDisc = elementwise_add(self.totBenefitsExtDisc, flow[2])

        return self

    def update(self, bcn: Bcn, flow: FlowType):
        return self
    
    def updateAllFlows(self, bcn: Bcn, flowsList):
        return self


class OptionalCashFlow(CashFlow):
    """
    Represents an optional cash flow in the output object.
    """

    def __init__(self, altID, tag, units, studyPeriod):
        default = [CostType(0)] * (studyPeriod + 1)

        self.altID = altID
        self.tag = tag

        self.totTagFlowDisc = default
        self.totTagQ = default
        self.quantUnits = units

    def add(self, bcn, flow):
        self.totTagFlowDisc = elementwise_add(self.totTagFlowDisc, flow[2])
        self.totTagQ = elementwise_add(self.totTagFlowDisc, flow[0])

        return self

    def update(self, bcn, flow):
        """To be added later for updating optional cash flow."""
        return self