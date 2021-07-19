from functools import reduce
from unittest import TestCase

from API.objects.Bcn import Bcn
from API.objects.CashFlow import CashFlow
from API.serializers.CashFlowSerializer import CashFlowSerializer


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
            bcnInvestBool=False,
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
        bcn0_expected = [0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        bcn1_expected = [0, 1050, 1102.5, 1157.625, 1215.50625, 1276.2815625, 1340.095640625, 1407.10042265625,
                         1477.45544378906, 1551.32821597852, 1628.89462677744]

        # When
        bcn0_result, _, _ = self.bcn0.cashFlows(10, 0.03)
        bcn1_result, _, _ = self.bcn1.cashFlows(10, 0.03)

        # Expect
        self.assertEquals(len(bcn0_expected), len(bcn0_result))
        self.assertEquals(len(bcn1_expected), len(bcn1_result))

        for x, y in zip(bcn0_expected, bcn0_result):
            self.assertAlmostEqual(x, y, 2)
        for x, y in zip(bcn1_expected, bcn1_result):
            self.assertAlmostEqual(x, y, 2)

    def test_values(self):
        # Given
        bcn0_expected = [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        bcn1_expected = [0, 94.0905, 101.75887575, 110.052224123625, 119.0214803897, 128.721731041461, 139.21255212134,
                         150.558375119229, 162.828882691447, 176.099436630799, 190.45154071621]

        bcn0_quantities = [0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        bcn1_quantities = [0, 1050, 1102.5, 1157.625, 1215.50625, 1276.2815625, 1340.095640625, 1407.10042265625,
                           1477.45544378906, 1551.32821597852, 1628.89462677744]

        # When
        bcn0_values = self.bcn0.values(10, bcn0_quantities)
        bcn1_values = self.bcn1.values(10, bcn1_quantities)

        # Expect
        self.assertEquals(len(bcn0_expected), len(bcn0_values))
        self.assertEquals(len(bcn1_expected), len(bcn1_values))

        for x, y in zip(bcn0_expected, bcn0_values):
            self.assertAlmostEqual(x, y, 2)
        for x, y in zip(bcn1_expected, bcn1_values):
            self.assertAlmostEqual(x, y, 2)

    def test_cash_flow_returns_values(self):
        # Given
        expected = [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, -133.333333333]

        # When
        _, result, _ = self.bcn0.cashFlows(10, 0.03)

        # Expect
        for x, y in zip(expected, result):
            self.assertAlmostEqual(x, y, 2)

    def test_discounted_values(self):
        # Given

        # When

        # Expect
        pass

    def test_bcn_1(self):
        print(self.bcn1.cashFlows(10, 0.03))

    def test_bcn_0(self):
        print(self.bcn0.cashFlows(10, 0.03))

    def test_totals(self):
        def elementwise(operator, list1, list2):
            return list(map(operator, list1, list2))

        values = list(map(lambda bcn: bcn.cashFlows(10, 0.03), [self.bcn0, self.bcn1]))
        totals = list(
            reduce(
                lambda x, y: (
                    elementwise(float.__add__, x[0], y[0]),
                    elementwise(float.__add__, x[1], y[1]),
                    elementwise(float.__add__, x[2], y[2])),
                values)
        )

        bcnflows = {bcn: bcn.cashFlows(10, 0.03) for bcn in [self.bcn0, self.bcn1]}

        output = CashFlow(0, bcnflows)

        output.print()

        serializer = CashFlowSerializer(output)
        print(serializer.data)


