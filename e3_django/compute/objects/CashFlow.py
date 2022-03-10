import operator

from API.objects import Bcn
from API.variables import CostType, FlowType

# Static Variables
COST = "Cost"
BENEFIT = "Benefit"


def elementwise_add(x, y):
    """
    Function that accepts two lists and adds them together element-wise.

    :param x: A list to add.
    :param y: A list to add.
    :return: A list comprised of the given lists added together element-wise.
    """
    return list(map(operator.add, x, y))


def bcn_type(bcn_type_param: str):
    """
    Decorator to denote whether a method should run only when a BCN has the correct type.

    :param bcn_type_param: The BCN type to allow the function to run.
    :return: The wrapped decorator function.
    """
    def inner_decorator(f):
        def wrapped(self, bcn_type_var: str, flow: FlowType):
            if bcn_type_param == bcn_type_var:
                f(self, flow)

        return wrapped
    return inner_decorator


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


class RequiredCashFlow(CashFlow):
    """
    Represents the required cash flow objects in the user output.
    """

    def __init__(self, alt: int, study_period: int):
        default = [CostType(0)] * (study_period + 1)

        # List of BCNs that this cash flow contains.
        self.bcn_list = []

        # The alternative ID that this cash flow is associated with.
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

    @bcn_type(COST)
    def add_base_cost(self, flow: FlowType):
        self.totCostNonDisc = elementwise_add(self.totCostNonDisc, flow[1])
        self.totCostDisc = elementwise_add(self.totCostDisc, flow[2])

    @bcn_type(BENEFIT)
    def add_base_benefits(self, flow: FlowType):
        self.totBenefitsNonDisc = elementwise_add(self.totBenefitsNonDisc, flow[1])
        self.totBenefitsDisc = elementwise_add(self.totBenefitsDisc, flow[2])

    @bcn_type(COST)
    def add_invest_cost(self, flow: FlowType):
        self.totCostsNonDiscInv = elementwise_add(self.totCostsNonDiscInv, flow[1])
        self.totCostsDiscInv = elementwise_add(self.totCostsDiscInv, flow[2])

    @bcn_type(BENEFIT)
    def add_invest_benefits(self, flow: FlowType):
        self.totBenefitsNonDiscInv = elementwise_add(self.totBenefitsNonDiscInv, flow[1])
        self.totBenefitsDiscInv = elementwise_add(self.totBenefitsDiscInv, flow[2])

    @bcn_type(COST)
    def add_non_invest_cost(self, flow: FlowType):
        self.totCostNonDiscNonInv = elementwise_add(self.totCostNonDiscNonInv, flow[1])
        self.totCostDiscNonInv = elementwise_add(self.totCostDiscNonInv, flow[2])

    @bcn_type(BENEFIT)
    def add_non_invest_benefits(self, flow: FlowType):
        self.totBenefitsNonDiscNonInv = elementwise_add(self.totBenefitsNonDiscNonInv, flow[1])
        self.totBenefitsDiscNonInv = elementwise_add(self.totBenefitsDiscNonInv, flow[2])

    @bcn_type(COST)
    def add_direct_cost(self, flow: FlowType):
        self.totCostDir = elementwise_add(self.totCostDir, flow[1])
        self.totCostDirDisc = elementwise_add(self.totCostDirDisc, flow[2])

    @bcn_type(BENEFIT)
    def add_direct_benefits(self, flow: FlowType):
        self.totBenefitsDir = elementwise_add(self.totBenefitsDir, flow[1])
        self.totBenefitsDirDisc = elementwise_add(self.totBenefitsDirDisc, flow[2])

    @bcn_type(COST)
    def add_indirect_cost(self, flow: FlowType):
        self.totCostInd = elementwise_add(self.totCostInd, flow[1])
        self.totCostIndDisc = elementwise_add(self.totCostIndDisc, flow[2])

    @bcn_type(BENEFIT)
    def add_indirect_benefits(self, flow: FlowType):
        self.totBenefitsInd = elementwise_add(self.totBenefitsInd, flow[1])
        self.totBenefitsIndDisc = elementwise_add(self.totBenefitsIndDisc, flow[2])

    @bcn_type(COST)
    def add_external_cost(self, flow: FlowType):
        self.totCostExt = elementwise_add(self.totCostExt, flow[1])
        self.totCostExtDisc = elementwise_add(self.totCostExtDisc, flow[2])

    @bcn_type(BENEFIT)
    def add_external_benefits(self, flow: FlowType):
        self.totBenefitsExt = elementwise_add(self.totBenefitsExt, flow[1])
        self.totBenefitsExtDisc = elementwise_add(self.totBenefitsExtDisc, flow[2])

    def add(self, bcn: Bcn, flow: FlowType):
        self.bcn_list.append(bcn)

        self.add_base_cost(bcn.bcnType, flow)
        self.add_base_benefits(bcn.bcnType, flow)

        if bcn.bcnInvestBool:
            self.add_invest_cost(bcn.bcnType, flow)
            self.add_invest_benefits(bcn.bcnType, flow)
        else:
            self.add_non_invest_cost(bcn.bcnType, flow)
            self.add_non_invest_benefits(bcn.bcnType, flow)

        if bcn.bcnSubType == "Direct":
            self.add_direct_cost(bcn.bcnType, flow)
            self.add_direct_benefits(bcn.bcnType, flow)
        elif bcn.bcnSubType == "Indirect":
            self.add_indirect_cost(bcn.bcnType, flow)
            self.add_indirect_benefits(bcn.bcnType, flow)
        else:
            self.add_external_cost(bcn.bcnType, flow)
            self.add_external_benefits(bcn.bcnType, flow)

        return self

    def __repr__(self):
        return str(self.__dict__)


class OptionalCashFlow(CashFlow):
    """
    Represents an optional cash flow in the output object.
    """

    def __init__(self, altID, tag, units, studyPeriod):
        default = [CostType(0)] * (studyPeriod + 1)

        # ID of the alternative this cash flow is associated with.
        self.altID = altID

        # Optional tag this cash flow is associated with.
        self.tag = tag

        # Total discount flow that will be mutated by the add method.
        self.totTagFlowDisc = default

        # Total quantity that will be mutated by the add method.
        self.totTagQ = default

        # Quantity units of the optoinal.
        self.quantUnits = units

    def add(self, bcn, flow):
        """
        Add the given BCN to this optional cash flow. Raises ValueError if the BCN is a part of this optional.

        :param bcn: The BCN object being added.
        :param flow: The BCN cash flow values to add.
        :return: This cash flow instance.
        """
        if self.tag not in bcn.bcnTag:
            raise ValueError(f"Optional of tag {self.tag} cannot accept BCN with tags {bcn.bcnTag}")

        self.totTagFlowDisc = elementwise_add(self.totTagFlowDisc, flow[2])
        self.totTagQ = elementwise_add(self.totTagQ, flow[0])

        return self

    def __repr__(self):
        return str(self.__dict__)