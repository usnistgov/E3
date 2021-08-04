from decimal import Decimal
from unittest import TestCase

from API.objects import Bcn
from API.objects import RequiredCashFlow
from API.objects.Bcn import create_list
from API.variables import CostType

PLACES = Decimal(10) ** -4


class NewBcnTest(TestCase):
    def setUp(self):
        self.bcn0 = Bcn(
            10,
            bcnID=0,
            altID=[0],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="BCN 1",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=False,
            bcnInvestBool=True,
            rvBool=True,
            bcnLife=30,
            recurBool=False,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=Decimal("2"),
            quant=Decimal("100"),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None
        )

        self.bcn1 = Bcn(
            10,
            bcnID=1,
            altID=[0, 1],
            bcnType="Cost",
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
            recurVarRate="percDelta",
            recurVarValue=Decimal("0.03"),
            recurEndDate=None,
            valuePerQ=Decimal("0.087"),
            quant=Decimal("1000"),
            quantVarRate="percDelta",
            quantVarValue=Decimal("0.05"),
            quantUnit="kWh"
        )

        self.required_flow = RequiredCashFlow(0, 10) \
            .add(self.bcn0, self.bcn0.cash_flows(10, Decimal("0.03"))) \
            .add(self.bcn1, self.bcn1.cash_flows(10, Decimal("0.03")))

    def test_create_array(self):
        # Given
        expected1 = [CostType(x) for x in [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        expected2 = [CostType(x) for x in [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        # When
        actual1 = create_list(10, 0)
        actual2 = create_list(10, 1)

        # Expect
        assert actual1 == expected1
        assert actual2 == expected2

    def test_quantities(self):
        # Given
        expected = [0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # When
        quantities = self.bcn0.quantities(10)

        # Expect
        assert quantities == expected

    def test_cash_flow_returns_quantities(self):
        # Given
        bcn0_expected = [CostType(x).quantize(PLACES) for x in [0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        bcn1_expected = [CostType(x).quantize(PLACES) for x in
                         ["0", "1050", "1102.5", "1157.625", "1215.50625", "1276.2815625", "1340.095640625",
                          "1407.10042265625", "1477.45544378906", "1551.32821597852", "1628.89462677744"]]

        # When
        bcn0_result, _, _ = self.bcn0.cash_flows(10, Decimal("0.03"))
        bcn1_result, _, _ = self.bcn1.cash_flows(10, Decimal("0.03"))

        bcn0_result = [x.quantize(PLACES) for x in bcn0_result]
        bcn1_result = [x.quantize(PLACES) for x in bcn1_result]

        # Expect
        assert bcn0_result == bcn0_expected
        assert bcn1_result == bcn1_expected

    def test_values(self):
        # Given
        bcn0_expected = [CostType(x).quantize(PLACES) for x in [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        bcn1_expected = [CostType(x).quantize(PLACES) for x in
                         ["0", "94.0905", "101.75887575", "110.052224123625", "119.0214803897", "128.721731041461",
                          "139.21255212134", "150.558375119229", "162.828882691447", "176.099436630799",
                          "190.45154071621"]]

        bcn0_quantities = [CostType(x) for x in [0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        bcn1_quantities = [CostType(x) for x in
                           ["0", "1050", "1102.5", "1157.625", "1215.50625", "1276.2815625", "1340.095640625",
                            "1407.10042265625", "1477.45544378906", "1551.32821597852", "1628.89462677744"]]

        # When
        bcn0_values = [x.quantize(PLACES) for x in self.bcn0.values(10, bcn0_quantities)]
        bcn1_values = [x.quantize(PLACES) for x in self.bcn1.values(10, bcn1_quantities)]

        # Expect
        assert bcn0_values == bcn0_expected
        assert bcn1_values == bcn1_expected

    def test_cash_flow_returns_values(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, -133.333333333]]

        # When
        _, actual, _ = self.bcn0.cash_flows(10, Decimal("0.03"))
        actual = [x.quantize(PLACES) for x in actual]

        # Expect
        assert actual == expected

    def test_discounted_values(self):
        # Given
        bcn0_expected = [CostType(x).quantize(PLACES) for x in
                         ["0", "194.174757281553", "0", "0", "0", "0", "0", "0", "0", "0", "-99.21252199"]]
        bcn1_expected = [CostType(x).quantize(PLACES) for x in
                         ["0", "91.35", "95.9175", "100.713375", "105.7490438", "111.0364959", "116.5883207",
                          "122.4177368", "128.5386236", "134.9655548", "141.7138325"]]

        # When
        _, _, bcn0_result = self.bcn0.cash_flows(10, Decimal("0.03"))
        _, _, bcn1_result = self.bcn1.cash_flows(10, Decimal("0.03"))

        bcn0_result = [x.quantize(PLACES) for x in bcn0_result]
        bcn1_result = [x.quantize(PLACES) for x in bcn1_result]

        # Expect
        assert bcn0_result == bcn0_expected
        assert bcn1_result == bcn1_expected

    def test_required_cash_flow_tot_cost_non_disc(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    ["0", "294.0905", "101.7588758", "110.0522241", "119.0214804", "128.721731", "139.2125521",
                     "150.5583751", "162.8288827", "176.0994366", "57.11820742"]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostNonDisc]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_cost_disc(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    ["0", "285.5247573", "95.9175", "100.713375", "105.7490438", "111.0364959", "116.5883207",
                     "122.4177368", "128.5386236", "134.9655548", "42.50131057"]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostDisc]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_cost_non_disc_inv(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, "-133.33333333"]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostsNonDiscInv]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_cost_disc_inv(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, "194.1747573", 0, 0, 0, 0, 0, 0, 0, 0, "-99.21252199"]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostsDiscInv]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_cost_non_disc_non_inv(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, "94.0905", "101.7588758", "110.0522241", "119.0214804", "128.721731", "139.2125521",
                     "150.5583751", "162.8288827", "176.0994366", "190.4515407"]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostNonDiscNonInv]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_cost_disc_non_inv(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, "91.35", "95.9175", "100.713375", "105.7490438", "111.0364959", "116.5883207", "122.4177368",
                     "128.5386236", "134.9655548", "141.7138325"]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostDiscNonInv]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_benefits_non_disc(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totBenefitsNonDisc]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_benefits_disc(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totBenefitsDisc]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_cost_dir(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, "-133.33333333"]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostDir]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_cost_ind(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, "94.0905", "101.7588758", "110.0522241", "119.0214804", "128.721731", "139.2125521",
                     "150.5583751", "162.8288827", "176.0994366", "190.4515407"]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostInd]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_cost_ext(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostExt]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_cost_dir_disc(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, "194.1747573", 0, 0, 0, 0, 0, 0, 0, 0, "-99.21252199"]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostDirDisc]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_cost_ind_disc(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, "91.35", "95.9175", "100.713375", "105.7490438", "111.0364959", "116.5883207", "122.4177368",
                     "128.5386236", "134.9655548", "141.7138325"]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostIndDisc]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_cost_ext_disc(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totCostExtDisc]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_benefits_dir(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totBenefitsDir]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_benefits_ind(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totBenefitsInd]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_benefits_ext(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totBenefitsExt]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_benefits_dir_disc(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totBenefitsDirDisc]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_benefits_ind_disc(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totBenefitsIndDisc]

        # Expect
        assert actual == expected

    def test_required_cash_flow_tot_benefits_ext_disc(self):
        # Given
        expected = [CostType(x).quantize(PLACES) for x in
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        # When
        actual = [x.quantize(PLACES) for x in self.required_flow.totBenefitsExtDisc]

        # Expect
        assert actual == expected

    def test_residual_value(self):
        # Given
        values = [CostType(x) for x in [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        expected = [CostType(x).quantize(PLACES) for x in [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, "-133.333333333"]]

        # When
        actual = [CostType(x).quantize(PLACES) for x in self.bcn0.residual_value(10, values)]

        # Expect
        assert actual == expected

    def test_residual_value_study_period_greater_than_life(self):
        # Given
        values = [CostType(x) for x in [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        expected = [CostType(x).quantize(PLACES) for x in [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        bcn = Bcn(
            10,
            bcnID=0,
            altID=[0],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="BCN 1",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=False,
            bcnInvestBool=True,
            rvBool=True,
            bcnLife=5,
            recurBool=False,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=Decimal("2"),
            quant=Decimal("100"),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None
        )

        # When
        actual = [CostType(x).quantize(PLACES) for x in bcn.residual_value(10, values)]

        # Expect
        assert actual == expected


    def test_residual_value_study_period_equal_to_life(self):
        # Given
        values = [CostType(x) for x in [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        expected = [CostType(x).quantize(PLACES) for x in [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        bcn = Bcn(
            10,
            bcnID=0,
            altID=[0],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="BCN 1",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=False,
            bcnInvestBool=True,
            rvBool=True,
            bcnLife=10,
            recurBool=False,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=Decimal("2"),
            quant=Decimal("100"),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None
        )

        # When
        actual = [CostType(x).quantize(PLACES) for x in bcn.residual_value(10, values)]

        # Expect
        assert actual == expected
