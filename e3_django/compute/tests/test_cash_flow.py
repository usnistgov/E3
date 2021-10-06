from unittest import TestCase

from API.objects import Bcn
from API.variables import CostType
from compute.objects.CashFlow import elementwise_add, RequiredCashFlow, OptionalCashFlow


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
            bcnType="Benefit",
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
            bcnType="Benefit",
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
        self.required_flow.add_base_cost("Benefit", self.flow)

        # Expect
        self.assertDefault()

    def test_add_base_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_base_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_base_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_base_benefits("Benefit", self.flow)

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
        self.required_flow.add_invest_cost("Benefit", self.flow)

        # Expect
        self.assertDefault()

    def test_add_invest_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_invest_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_invest_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_invest_benefits("Benefit", self.flow)

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
        self.required_flow.add_non_invest_cost("Benefit", self.flow)

        # Expect
        self.assertDefault()

    def test_add_non_invest_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_non_invest_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_non_invest_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_non_invest_benefits("Benefit", self.flow)

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
        self.required_flow.add_direct_cost("Benefit", self.flow)

        # Expect
        self.assertDefault()

    def test_add_direct_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_direct_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_direct_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_direct_benefits("Benefit", self.flow)

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
        self.required_flow.add_indirect_cost("Benefit", self.flow)

        # Expect
        self.assertDefault()

    def test_add_indirect_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_indirect_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_indirect_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_indirect_benefits("Benefit", self.flow)

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
        self.required_flow.add_external_cost("Benefit", self.flow)

        # Expect
        self.assertDefault()

    def test_add_external_benefits_when_type_is_cost(self):
        # When
        self.required_flow.add_external_benefits("Cost", self.flow)

        # Expect
        self.assertDefault()

    def test_add_external_benefits_when_type_is_benefits(self):
        # When
        self.required_flow.add_external_benefits("Benefit", self.flow)

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


class RequiredCashFlowSecondCaseTest(TestCase):
    def setUp(self):
        self.bcns = {
            "bcn0": Bcn(
                10,
                bcnID=0,
                altID=[0],
                bcnType="Cost",
                bcnSubType="Direct",
                bcnName="COST 1",
                bcnTag="Tag 1",
                initialOcc=1,
                bcnInvestBool=True,
                rvBool=True,
                bcnLife=30,
                recurBool=None,
                recurInterval=None,
                recurVarRate=None,
                recurVarValue=None,
                recurEndDate=None,
                valuePerQ=CostType("2"),
                quant=CostType("100"),
                quantVarRate=None,
                quantVarValue=None,
                quantUnit="m^3"
            ),
            "bcn1": Bcn(
                10,
                bcnID=1,
                altID=[0, 1],
                bcnType="Cost",
                bcnSubType="Indirect",
                bcnName="COST 2",
                bcnTag=None,
                initialOcc=1,
                bcnInvestBool=False,
                rvBool=False,
                bcnLife=None,
                recurBool=True,
                recurInterval=1,
                recurVarRate="Percent Delta Timestep X-1",
                recurVarValue=CostType("0.03"),
                recurEndDate=None,
                valuePerQ=CostType("0.087"),
                quant=CostType("1000"),
                quantVarRate="Percent Delta Timestep X-1",
                quantVarValue=CostType("0.05"),
                quantUnit="kWh"
            ),
            "bcn2": Bcn(
                10,
                bcnID=2,
                altID=[1, 2],
                bcnType="Cost",
                bcnSubType="Externality",
                bcnName="EXT 2",
                bcnTag=None,
                initialOcc=5,
                bcnInvestBool=True,
                rvBool=False,
                bcnLife=6,
                recurBool=False,
                recurInterval=None,
                recurVarRate=None,
                recurVarValue=None,
                recurEndDate=None,
                valuePerQ=CostType("1"),
                quant=CostType("500"),
                quantVarRate=None,
                quantVarValue=None,
                quantUnit=None
            ),
            "bcn3": Bcn(
                10,
                bcnID=3,
                altID=[1],
                bcnType="Benefit",
                bcnSubType="Direct",
                bcnName="Benefit 1",
                bcnTag="Tag 1",
                initialOcc=2,
                bcnInvestBool=False,
                rvBool=False,
                bcnLife=None,
                recurBool=True,
                recurInterval=2,
                recurVarRate="Percent Delta Timestep X-1",
                recurVarValue=None,
                recurEndDate=None,
                valuePerQ=CostType("1"),
                quant=CostType("30"),
                quantVarRate="Percent Delta Timestep X-1",
                quantVarValue=[0, 0.01, 0.01, 0.02, 0.02, 0.01, -0.01, 0.02, 0.01, 0, -0.02],
                quantUnit="m^3"
            ),
            "bcn4": Bcn(
                10,
                bcnID=4,
                altID=[2],
                bcnType="Benefit",
                bcnSubType="Indirect",
                bcnName="Benefit 2",
                bcnTag=None,
                initialOcc=3,
                bcnRealBool=False,
                bcnInvestBool=False,
                rvBool=False,
                bcnLife=None,
                recurBool=True,
                recurInterval=1,
                recurVarRate="Percent Delta Timestep X-1",
                recurVarValue=[0, 0.04, 0.05, 0.02, 0.01, -0.03, 0.06, 0.02, -0.01, -0.03, 0.09],
                recurEndDate=6,
                valuePerQ=CostType("3"),
                quant=CostType("350.5"),
                quantVarRate=None,
                quantVarValue=None,
                quantUnit="tonnes"
            ),
            "bcn5": Bcn(
                10,
                bcnID=5,
                altID=[1, 2],
                bcnType="Benefit",
                bcnSubType="Indirect",
                bcnName="Benefit 3",
                bcnTag="Tag 1",
                initialOcc=0,
                bcnInvestBool=False,
                rvBool=False,
                bcnLife=None,
                recurBool=True,
                recurInterval=1,
                recurVarRate="Percent Delta Timestep X-1",
                recurVarValue=CostType("0.01"),
                recurEndDate=7,
                valuePerQ=CostType("0.01"),
                quant=CostType("90"),
                quantVarRate="Percent Delta Timestep X-1",
                quantVarValue=CostType("-0.03"),
                quantUnit="m^3"
            ),
            "bcn6": Bcn(
                10,
                bcnID=6,
                altID=[0],
                bcnType="Benefit",
                bcnSubType="Indirect",
                bcnName="Benefit 4",
                bcnTag=None,
                initialOcc=6,
                bcnInvestBool=False,
                rvBool=False,
                bcnLife=None,
                recurBool=False,
                recurInterval=None,
                recurVarRate=None,
                recurVarValue=None,
                recurEndDate=None,
                valuePerQ=CostType("0.5"),
                quant=CostType("250"),
                quantVarRate=None,
                quantVarValue=None,
                quantUnit=None
            ),
            "bcn7": Bcn(
                10,
                bcnID=7,
                altID=[2],
                bcnType="Cost",
                bcnSubType="Indirect",
                bcnName="Cost 3",
                bcnTag="Tag 2",
                initialOcc=0,
                bcnInvestBool=True,
                rvBool=True,
                bcnLife=4,
                recurBool=True,
                recurInterval=5,
                recurVarRate="Percent Delta Timestep X-1",
                recurVarValue=CostType("0.01"),
                recurEndDate=None,
                valuePerQ=CostType("1"),
                quant=CostType("100"),
                quantVarRate=None,
                quantVarValue=None,
                quantUnit="m^2"
            ),
            "bcn8": Bcn(
                10,
                bcnID=8,
                altID=[1, 2],
                bcnType="Non-Monetary",
                bcnSubType="Direct",
                bcnName="NM 1",
                bcnTag="Tag 3",
                initialOcc=0,
                bcnInvestBool=False,
                rvBool=False,
                bcnLife=None,
                recurBool=True,
                recurInterval=1,
                recurVarRate=None,
                recurVarValue=None,
                recurEndDate=None,
                valuePerQ=None,
                quant=CostType("100"),
                quantVarRate=None,
                quantVarValue=None,
                quantUnit="m"
            )
        }

    def test_required_flow(self):
        required = {}
        for bcn in self.bcns.values():
            for alt in bcn.altID:
                flow = bcn.cash_flows(10, CostType("0.03"))

                print(f"{alt} {bcn.bcnID}")

                print("---Flow---")
                for x in flow:
                    print(f"{[str(y) for y in x]}")

                required[alt] = required \
                    .get(alt, RequiredCashFlow(alt, 10)) \
                    .add(bcn, flow)

        for x in required.values():
            x.print()

        print(f"Alternative Summary Sum: {sum(required[0].totCostDisc)}")


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
