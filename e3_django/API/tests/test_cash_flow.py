from unittest import TestCase

from API.objects import RequiredCashFlow, Bcn
from API.objects.CashFlow import elementwise_add, OptionalCashFlow
from API.variables import CostType


class GeneralCashFlowTest(TestCase):
    def setUp(self):
        self.x = [1, 2, 3, 4]
        self.y = [5, 6, 7, 8]

    def test_elementwise_add_returns_list(self):
        # When
        result = elementwise_add(self.x, self.y)

        # Expect
        assert isinstance(result, list)

    def test_elementwise_add_returns_correct_result(self):
        # When
        result = elementwise_add(self.x, self.y)

        # Expect
        assert len(result) == 4
        assert result == [6, 8, 10, 12]


class RequiredCashFlowTest(TestCase):
    def setUp(self):
        self.default = [CostType(0)] * 5
        self.flow = ([CostType(1)] * 5, [CostType(2)] * 5, [CostType(3)] * 5)
        self.required_flow = RequiredCashFlow(1, 4)
        self.bcn0 = Bcn(
            4,
            bcnID=0,
            altID=[0],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="BCN 1",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=False,
            bcnInvestBool=True,
            rvBool=False,
            bcnLife=30,
            recurBool=False,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=CostType("2"),
            quant=CostType("100"),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None
        )
        self.bcn1 = Bcn(
            4,
            bcnID=1,
            altID=[0, 1],
            bcnType="Benefits",
            bcnSubType="Indirect",
            bcnName="BCN 2",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate="Percent Delta Timestep X-1",
            recurVarValue=CostType("0"),
            recurEndDate=None,
            valuePerQ=CostType("0"),
            quant=CostType("2"),
            quantVarRate="Percent Delta Timestep X-1",
            quantVarValue=CostType("0"),
            quantUnit="kWh"
        )
        self.bcn2 = Bcn(
            4,
            bcnID=1,
            altID=[0, 1],
            bcnType="Cost",
            bcnSubType="Other",
            bcnName="BCN 2",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate="Percent Delta Timestep X-1",
            recurVarValue=CostType("0"),
            recurEndDate=None,
            valuePerQ=CostType("0"),
            quant=CostType("2"),
            quantVarRate="Percent Delta Timestep X-1",
            quantVarValue=CostType("0"),
            quantUnit="kWh"
        )
        self.bcn3 = Bcn(
            4,
            bcnID=1,
            altID=[0, 1],
            bcnType="Benefits",
            bcnSubType="Other",
            bcnName="BCN 2",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate="Percent Delta Timestep X-1",
            recurVarValue=CostType("0"),
            recurEndDate=None,
            valuePerQ=CostType("0"),
            quant=CostType("2"),
            quantVarRate="Percent Delta Timestep X-1",
            quantVarValue=CostType("0"),
            quantUnit="kWh"
        )

    def test_initializer(self):
        # Given
        expected = [CostType(0)] * 6
        alt_id = 1

        # When
        required_flow = RequiredCashFlow(alt_id, 5)

        # Expect
        assert required_flow.bcn_list == []
        assert required_flow.altID == alt_id

        assert required_flow.totCostNonDisc == expected
        assert required_flow.totCostDisc == expected
        assert required_flow.totBenefitsNonDisc == expected
        assert required_flow.totBenefitsDisc == expected

        assert required_flow.totCostsNonDiscInv == expected
        assert required_flow.totCostsDiscInv == expected
        assert required_flow.totBenefitsNonDiscInv == expected
        assert required_flow.totBenefitsDiscInv == expected

        assert required_flow.totCostNonDiscNonInv == expected
        assert required_flow.totCostDiscNonInv == expected
        assert required_flow.totBenefitsNonDiscNonInv == expected
        assert required_flow.totBenefitsDiscNonInv == expected

        assert required_flow.totCostDir == expected
        assert required_flow.totCostDirDisc == expected
        assert required_flow.totBenefitsDir == expected
        assert required_flow.totBenefitsDirDisc == expected

        assert required_flow.totCostInd == expected
        assert required_flow.totCostIndDisc == expected
        assert required_flow.totBenefitsInd == expected
        assert required_flow.totBenefitsIndDisc == expected

        assert required_flow.totCostExt == expected
        assert required_flow.totCostExtDisc == expected
        assert required_flow.totBenefitsExt == expected
        assert required_flow.totBenefitsExtDisc == expected

    def assertDefault(self, exclude_list: list = None):
        base_exclude = ["altID", "bcn_list"]
        if exclude_list is None:
            exclude_list = []

        for key, value in self.required_flow.__dict__.items():
            if key in base_exclude or key in exclude_list:
                continue

            assert value == self.default

    def test_add_base_cost_when_type_is_cost(self):
        # When
        self.required_flow.add_base_cost("Cost", self.flow)

        # Expect
        assert self.required_flow.totCostNonDisc == self.flow[1]
        assert self.required_flow.totCostDisc == self.flow[2]
        self.assertDefault(["totCostNonDisc", "totCostDisc"])

    def test_add_base_cost_when_type_is_benefits(self):
        # When
        self.required_flow.add_base_cost("Benefits", self.flow)

        # Expect
        self.assertDefault()

    def test_add_base_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_base_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_base_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_base_benefits("Benefits", self.flow)

        # Expect
        assert self.required_flow.totBenefitsNonDisc == self.flow[1]
        assert self.required_flow.totBenefitsDisc == self.flow[2]
        self.assertDefault(["totBenefitsNonDisc", "totBenefitsDisc"])

    def test_add_invest_cost_when_type_is_cost(self):
        # When
        self.required_flow.add_invest_cost("Cost", self.flow)

        # Expect
        assert self.required_flow.totCostsNonDiscInv == self.flow[1]
        assert self.required_flow.totCostsDiscInv == self.flow[2]
        self.assertDefault(["totCostsNonDiscInv", "totCostsDiscInv"])

    def test_add_invest_cost_when_type_is_benefits(self):
        # When
        self.required_flow.add_invest_cost("Benefits", self.flow)

        # Expect
        self.assertDefault()

    def test_add_invest_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_invest_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_invest_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_invest_benefits("Benefits", self.flow)

        # Expect
        assert self.required_flow.totBenefitsNonDiscInv == self.flow[1]
        assert self.required_flow.totBenefitsDiscInv == self.flow[2]
        self.assertDefault(["totBenefitsNonDiscInv", "totBenefitsDiscInv"])

    def test_add_non_invest_cost_when_type_is_cost(self):
        # When
        self.required_flow.add_non_invest_cost("Cost", self.flow)

        # Expect
        assert self.required_flow.totCostNonDiscNonInv == self.flow[1]
        assert self.required_flow.totCostDiscNonInv == self.flow[2]
        self.assertDefault(["totCostNonDiscNonInv", "totCostDiscNonInv"])

    def test_add_non_invest_cost_when_type_is_benefits(self):
        # When
        self.required_flow.add_non_invest_cost("Benefits", self.flow)

        # Expect
        self.assertDefault()

    def test_add_non_invest_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_non_invest_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_non_invest_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_non_invest_benefits("Benefits", self.flow)

        # Expect
        assert self.required_flow.totBenefitsNonDiscNonInv == self.flow[1]
        assert self.required_flow.totBenefitsDiscNonInv == self.flow[2]
        self.assertDefault(["totBenefitsNonDiscNonInv", "totBenefitsDiscNonInv"])

    def test_add_direct_cost_when_type_is_cost(self):
        # When
        self.required_flow.add_direct_cost("Cost", self.flow)

        # Expect
        assert self.required_flow.totCostDir == self.flow[1]
        assert self.required_flow.totCostDirDisc == self.flow[2]
        self.assertDefault(["totCostDir", "totCostDirDisc"])

    def test_add_direct_cost_when_type_is_benefits(self):
        # When
        self.required_flow.add_direct_cost("Benefits", self.flow)

        # Expect
        self.assertDefault()

    def test_add_direct_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_direct_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_direct_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_direct_benefits("Benefits", self.flow)

        # Expect
        assert self.required_flow.totBenefitsDir == self.flow[1]
        assert self.required_flow.totBenefitsDirDisc == self.flow[2]
        self.assertDefault(["totBenefitsDir", "totBenefitsDirDisc"])

    def test_add_indirect_cost_when_type_is_cost(self):
        # When
        self.required_flow.add_indirect_cost("Cost", self.flow)

        # Expect
        assert self.required_flow.totCostInd == self.flow[1]
        assert self.required_flow.totCostIndDisc == self.flow[2]
        self.assertDefault(["totCostInd", "totCostIndDisc"])

    def test_add_indirect_cost_when_type_is_benefits(self):
        # When
        self.required_flow.add_indirect_cost("Benefits", self.flow)

        # Expect
        self.assertDefault()

    def test_add_indirect_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_indirect_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_indirect_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_indirect_benefits("Benefits", self.flow)

        # Expect
        assert self.required_flow.totBenefitsInd == self.flow[1]
        assert self.required_flow.totBenefitsIndDisc == self.flow[2]
        self.assertDefault(["totBenefitsInd", "totBenefitsIndDisc"])

    def test_add_external_cost_when_type_is_cost(self):
        # When
        self.required_flow.add_external_cost("Cost", self.flow)

        # Expect
        assert self.required_flow.totCostExt == self.flow[1]
        assert self.required_flow.totCostExtDisc == self.flow[2]
        self.assertDefault(["totCostExt", "totCostExtDisc"])

    def test_add_external_cost_when_type_is_benefits(self):
        # When
        self.required_flow.add_external_cost("Benefits", self.flow)

        # Expect
        self.assertDefault()

    def test_add_external_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_external_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_external_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_external_benefits("Benefits", self.flow)

        # Expect
        assert self.required_flow.totBenefitsExt == self.flow[1]
        assert self.required_flow.totBenefitsExtDisc == self.flow[2]
        self.assertDefault(["totBenefitsExt", "totBenefitsExtDisc"])

    def test_add_appends_to_bcn_list(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)

        # Expect
        assert len(self.required_flow.bcn_list) == 1
        assert self.required_flow.bcn_list[0] == self.bcn0

    def test_add_appends_multiple_to_bcn_list(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)

        # Expect
        assert len(self.required_flow.bcn_list) == 2
        assert self.required_flow.bcn_list[0] == self.bcn0
        assert self.required_flow.bcn_list[1] == self.bcn1

    def test_add_sums_base_costs(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)

        # Expect
        assert self.required_flow.totCostNonDisc == [CostType(4)] * 5
        assert self.required_flow.totCostDisc == [CostType(6)] * 5

    def test_add_sums_base_benefits(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)

        # Expect
        assert self.required_flow.totBenefitsNonDisc == [CostType(2)] * 5
        assert self.required_flow.totBenefitsDisc == [CostType(3)] * 5

    def test_add_sums_invest_cost(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)

        # Expect
        assert self.required_flow.totCostsNonDiscInv == [CostType(4)] * 5
        assert self.required_flow.totCostsDiscInv == [CostType(6)] * 5

    def test_add_sums_invest_benefits(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)

        # Expect
        assert self.required_flow.totBenefitsNonDiscInv == [CostType(0)] * 5
        assert self.required_flow.totBenefitsDiscInv == [CostType(0)] * 5

    def test_add_sums_non_invest_costs(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)

        # Expect
        assert self.required_flow.totCostNonDiscNonInv == [CostType(0)] * 5
        assert self.required_flow.totCostDiscNonInv == [CostType(0)] * 5

    def test_add_sums_non_invest_benefits(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)

        # Expect
        assert self.required_flow.totBenefitsNonDiscNonInv == [CostType(2)] * 5
        assert self.required_flow.totBenefitsDiscNonInv == [CostType(3)] * 5

    def test_add_sums_direct_costs(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)

        # Expect
        assert self.required_flow.totCostDir == [CostType(4)] * 5
        assert self.required_flow.totCostDirDisc == [CostType(6)] * 5

    def test_add_sums_direct_benefits(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)

        # Expect
        assert self.required_flow.totBenefitsDir == [CostType(0)] * 5
        assert self.required_flow.totBenefitsDirDisc == [CostType(0)] * 5

    def test_add_sums_indirect_costs(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)

        # Expect
        assert self.required_flow.totCostInd == [CostType(0)] * 5
        assert self.required_flow.totCostIndDisc == [CostType(0)] * 5

    def test_add_sums_indirect_benefits(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)

        # Expect
        assert self.required_flow.totBenefitsInd == [CostType(2)] * 5
        assert self.required_flow.totBenefitsIndDisc == [CostType(3)] * 5

    def test_add_sums_external_costs(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)
        self.required_flow.add(self.bcn2, self.flow)
        self.required_flow.add(self.bcn3, self.flow)
        self.required_flow.add(self.bcn3, self.flow)


        # Expect
        assert self.required_flow.totCostExt == [CostType(2)] * 5
        assert self.required_flow.totCostExtDisc == [CostType(3)] * 5

    def test_add_sums_external_benefits(self):
        # When
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn0, self.flow)
        self.required_flow.add(self.bcn1, self.flow)
        self.required_flow.add(self.bcn2, self.flow)
        self.required_flow.add(self.bcn3, self.flow)
        self.required_flow.add(self.bcn3, self.flow)

        # Expect
        assert self.required_flow.totBenefitsExt == [CostType(4)] * 5
        assert self.required_flow.totBenefitsExtDisc == [CostType(6)] * 5

    def test_add_returns_self(self):
        # When
        cash_flow = self.required_flow.add(self.bcn0, self.flow)

        # Expect
        assert isinstance(cash_flow, RequiredCashFlow)
        assert cash_flow == self.required_flow


class OptionalCashFlowTest(TestCase):
    def setUp(self):
        self.flow = ([CostType(1)] * 5, [CostType(2)] * 5, [CostType(3)] * 5)
        self.optional_flow = OptionalCashFlow(1, "test_tag", "test_units", 4)

    def test_object_creation(self):
        # Expect
        assert isinstance(self.optional_flow, OptionalCashFlow)
        assert self.optional_flow.altID == 1
        assert self.optional_flow.tag == "test_tag"
        assert self.optional_flow.quantUnits == "test_units"
        assert self.optional_flow.totTagFlowDisc == [CostType("0")] * 5
        assert self.optional_flow.totTagQ == [CostType("0")] * 5

    def test_add_updates_correct_variables(self):
        # When
        self.optional_flow.add(None, self.flow)

        # Expect
        assert self.optional_flow.totTagFlowDisc == [CostType(3)] * 5
        assert self.optional_flow.totTagQ == [CostType(0)] * 5
