from decimal import Decimal
from unittest import TestCase

from API.objects.Bcn import Bcn, createArray
from API.objects.CashFlow import CashFlow
from API.serializers import CostType

PLACES = Decimal(10) ** -2


class NewBcnTest(TestCase):
    def setUp(self):
        self.bcn10 = Bcn(
            25,
            bcnID=10,
            altID=1,
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="Electricity Consumption",
            initialOcc=7,
            bcnRealBool=False,
            bcnInvestBool=False,
            rvBool=False,
            recurBool=True,
            recurInterval=1,
            recurVarRate="percDelta",
            recurVarValue=0.0,
            recurEndDate=25,
            valuePerQ=0.126,
            quant=9,
            quantVarRate="percDelta",
            quantVarValue=[0.00, 5.72, 0.85, 0.46, 0.31, 0.24, 0.19, 0.16, 0.14, 0.12, 0.11, 0.10, 0.09, 0.08, 0.07,
                           0.07, 0.06, 0.06],
            quantUnit="kwh"
        )

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
            valuePerQ=2,
            quant=100,
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
            recurVarValue=0.03,
            recurEndDate=None,
            valuePerQ=0.087,
            quant=1000,
            quantVarRate="percDelta",
            quantVarValue=0.05,
            quantUnit="kWh"
        )

    def test_create_array(self):
        # Given
        expected1 = [CostType(x) for x in [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        expected2 = [CostType(x) for x in [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

        # When
        actual1 = createArray(10, 0)
        actual2 = createArray(10, 1)

        # Expect
        self.assertEqual(expected1, actual1)
        self.assertEqual(expected2, actual2)

    def test_quantities(self):
        # Given
        expected = [0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        # When
        quantities = self.bcn0.quantities(10)

        # Expect
        self.assertEqual(len(expected), len(quantities))

        for x, y in zip(expected, quantities):
            self.assertAlmostEqual(x, y, 2)

    def test_cash_flow_returns_quantities(self):
        # Given
        bcn0_expected = [CostType(x) for x in [0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        bcn1_expected = [CostType(x) for x in [0, 1050, 1102.5, 1157.625, 1215.50625, 1276.2815625, 1340.095640625,
                                               1407.10042265625, 1477.45544378906, 1551.32821597852, 1628.89462677744]]

        # When
        bcn0_result, _, _ = self.bcn0.cashFlows(10, 0.03)
        bcn1_result, _, _ = self.bcn1.cashFlows(10, 0.03)

        # Expect
        self.assertEquals(len(bcn0_expected), len(bcn0_result))
        self.assertEquals(len(bcn1_expected), len(bcn1_result))

        for x, y in zip(bcn0_expected, bcn0_result):
            self.assertEqual(x.quantize(PLACES), y.quantize(PLACES))
        for x, y in zip(bcn1_expected, bcn1_result):
            self.assertEqual(x.quantize(PLACES), y.quantize(PLACES))

    def test_values(self):
        # Given
        bcn0_expected = [CostType(x) for x in [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        bcn1_expected = [CostType(x) for x in
                         [0, 94.0905, 101.75887575, 110.052224123625, 119.0214803897, 128.721731041461, 139.21255212134,
                          150.558375119229, 162.828882691447, 176.099436630799, 190.45154071621]]

        bcn0_quantities = [CostType(x) for x in [0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        bcn1_quantities = [CostType(x) for x in
                           [0, 1050, 1102.5, 1157.625, 1215.50625, 1276.2815625, 1340.095640625, 1407.10042265625,
                            1477.45544378906, 1551.32821597852, 1628.89462677744]]

        # When
        bcn0_values = self.bcn0.values(10, bcn0_quantities)
        bcn1_values = self.bcn1.values(10, bcn1_quantities)

        # Expect
        self.assertEqual(len(bcn0_expected), len(bcn0_values))
        self.assertEqual(len(bcn1_expected), len(bcn1_values))

        for x, y in zip(bcn0_expected, bcn0_values):
            self.assertAlmostEqual(x, y, 2)
        for x, y in zip(bcn1_expected, bcn1_values):
            self.assertAlmostEqual(x, y, 2)

    def test_cash_flow_returns_values(self):
        # Given
        expected = [CostType(x) for x in [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, -133.333333333]]

        # When
        _, result, _ = self.bcn0.cashFlows(10, 0.03)

        # Expect
        for x, y in zip(expected, result):
            self.assertAlmostEqual(x, y, 2)

    def test_discounted_values(self):
        # Given
        bcn0_expected = [CostType(x) for x in
                         [0, 194.174757281553, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        bcn1_expected = [CostType(x) for x in [0, 1050, 1102.5, 1157.625, 1215.50625, 1276.2815625, 1340.095640625,
                                               1407.10042265625, 1477.45544378906, 1551.32821597852, 1628.89462677744]]

        # When
        bcn0_result, _, _ = self.bcn0.cashFlows(10, 0.03)
        bcn1_result, _, _ = self.bcn1.cashFlows(10, 0.03)

        # Expect
        self.assertEquals(len(bcn0_expected), len(bcn0_result))
        self.assertEquals(len(bcn1_expected), len(bcn1_result))

        for x, y in zip(bcn0_expected, bcn0_result):
            self.assertEqual(x.quantize(PLACES), y.quantize(PLACES))
        for x, y in zip(bcn1_expected, bcn1_result):
            self.assertEqual(x.quantize(PLACES), y.quantize(PLACES))

    def test_cash_flow(self):
        expectedTotCostNonDisc = [CostType(x) for x in
                                  [0, 294.0905, 101.7588758, 110.0522241, 119.0214804, 128.721731, 139.2125521,
                                   150.5583751, 162.8288827, 176.0994366, 57.11820742]]
        expectedTotCostDisc = [CostType(x) for x in
                               [0, 285.5247573, 95.9175, 100.713375, 105.7490438, 111.0364959, 116.5883207, 122.4177368,
                                128.5386236, 134.9655548, 42.50131057]]
        expectedTotCostNonDiscInv = [CostType(x) for x in [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, -133.33333333]]

        cashflow = CashFlow(
            0,
            {
                self.bcn0: self.bcn0.cashFlows(10, 0.03),
                self.bcn1: self.bcn1.cashFlows(10, 0.03)
            },
            10)

        for x, y in zip(expectedTotCostNonDisc, cashflow.totCostNonDisc):
            self.assertEqual(x.quantize(PLACES), y.quantize(PLACES))
        for x, y in zip(expectedTotCostDisc, cashflow.totCostDisc):
            self.assertEqual(x.quantize(PLACES), y.quantize(PLACES))
        for x, y in zip(expectedTotCostNonDiscInv, cashflow.totCostsNonDiscInv):
            self.assertEqual(x.quantize(PLACES), y.quantize(PLACES))

        print(cashflow.totBenefitsIndDisc)

        for x in cashflow.totBenefitsIndDisc:
            self.assertEqual(0, x)
        for x in cashflow.totBenefitsExtDisc:
            self.assertEqual(0, x)
