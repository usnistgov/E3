from decimal import Decimal
from unittest import TestCase

import pytest

from API.objects import Bcn
from API.objects.AlternativeSummary import sir, bcr, net_savings, net_benefits, check_fraction, airr, payback_period, \
    ns_per_q, ns_per_pct_q, ns_elasticity

PLACES = Decimal(10) ** -13

AIRR_NOT_CALCULABLE = "AIRR Not Calculable"
INFINITY = "Infinity"
NOT_CALCULABLE = "Not Calculable"

class NewAlternativeSummaryFunctionTest(TestCase):
    def test_sir_infinity(self):
        result = sir(Decimal("431.304392192082"), Decimal("133.831872126668"), Decimal("94.9622352953234"),
                      Decimal("1148.99048312239"))
        assert result == INFINITY

    def test_sir_0(self):
        result = sir(Decimal("0"), Decimal("1148.99048"), Decimal("139.60787"), Decimal("1148.99048"))
        assert result == 0

    def test_sir_not_calculable(self):
        result = sir(Decimal("431.304392192082"), Decimal("1148.99048312239"), Decimal("94.9622352953234"),
                      Decimal("1148.99048312239"))
        assert result == NOT_CALCULABLE

    def test_sir(self):
        result = sir(Decimal("100"), Decimal("300"), Decimal("200"), Decimal("550"))
        assert result == Decimal("2.5")

    def test_bcr_not_calculable(self):
        result = bcr(Decimal("-301.340592511856"), Decimal("94.9622352953234"), Decimal("431.304392192082"))
        assert result == NOT_CALCULABLE

    def test_bcr(self):
        result = bcr(Decimal("4711.42470789861"), Decimal("431.304392192082"), Decimal("94.9622352953234"))
        assert result.quantize(PLACES) == Decimal("14.0078328312106")

    def test_bcr_infinity(self):
        result = bcr(Decimal("139.607870189127"), Decimal("0"), Decimal("139.607870189127"))
        assert result == INFINITY

    def test_net_savings(self):
        result1 = net_savings(Decimal("1243.95271841771"), Decimal("1580.29487531447"))
        result2 = net_savings(Decimal("1"), Decimal("0"))
        result3 = net_savings(Decimal("1"), Decimal("1"))

        assert result1.quantize(Decimal(10) ** -7) == Decimal("-336.3421569")
        assert result2 == Decimal("1")
        assert result3 == Decimal("0")

    def test_net_benefits(self):
        result = net_benefits(Decimal("0"), Decimal("1148.99048"), Decimal("0"), Decimal("1288.59835"))
        assert result == Decimal("139.60787")

    def test_check_fraction_normal(self):
        result = check_fraction(Decimal("2"), Decimal("2"))
        assert result == Decimal("1")

    def test_check_fraction_infinity(self):
        result = check_fraction(Decimal("1"), Decimal("-2"))
        assert result == INFINITY

    def test_check_fraction_not_calculable(self):
        result = check_fraction(Decimal("-1"), Decimal("-2"))
        assert result == NOT_CALCULABLE

    def test_airr(self):
        result = airr(Decimal("1"), Decimal("0.05"), 10)
        assert result == Decimal("0.05")

        result = airr(Decimal("2.5"), Decimal("0.05"), 10)
        assert result.quantize(PLACES) == Decimal("0.150756137704478").quantize(PLACES)

    def test_airr_not_calculable(self):
        result = airr(Decimal("0"), Decimal("0.05"), 10)
        assert result == AIRR_NOT_CALCULABLE

    def test_airr_not_calculable_if_sir_infinity(self):
        result = airr(INFINITY, Decimal("0.05"), 10)
        assert result == AIRR_NOT_CALCULABLE

    def test_airr_not_calculable_if_sir_not_calculable(self):
        result = airr(NOT_CALCULABLE, Decimal("0.05"), 10)
        assert result == AIRR_NOT_CALCULABLE

    def test_payback_period_parameters_same_length(self):
        with pytest.raises(ValueError) as exec_info:
            payback_period([1, 1, 1], [2, 2])

        assert isinstance(exec_info.value, ValueError)

    def test_payback_period(self):
        index = payback_period([2, 2, 2, 0], [1, 1, 1, 1])
        assert index == 3

    def test_payback_period_default_is_none(self):
        index = payback_period([2], [1])
        assert index is INFINITY

    def test_ns_per_q_infinity(self):
        result1 = ns_per_q(Decimal("0"), Decimal("0"))
        result2 = ns_per_q(Decimal("1"), Decimal("0"))

        assert result1 == INFINITY
        assert result2 == INFINITY

    def test_ns_per_q(self):
        result1 = ns_per_q(Decimal("1"), Decimal("1"))
        result2 = ns_per_q(Decimal("1"), Decimal("2"))

        assert result1 == Decimal("1")
        assert result2 == Decimal("0.5")

    def test_ns_per_pct_q_infinity(self):
        result1 = ns_per_pct_q(Decimal("0"), Decimal("0"), Decimal("0"))
        result2 = ns_per_pct_q(Decimal("1"), Decimal("1"), Decimal("0"))

        assert result1 == INFINITY
        assert result2 == INFINITY

    def test_ns_per_pct_q(self):
        result1 = ns_per_pct_q(Decimal("1"), Decimal("4"), Decimal("2"))
        result2 = ns_per_pct_q(Decimal("1"), Decimal("1"), Decimal("1"))

        assert result1 == Decimal("0.5")
        assert result2 == Decimal("1")

    def test_ns_elasticity_infinity(self):
        result1 = ns_elasticity(Decimal("1"), Decimal("0"), Decimal("1"), Decimal("1"))
        result2 = ns_elasticity(Decimal("1"), Decimal("1"), Decimal("1"), Decimal("0"))

        assert result1 == INFINITY
        assert result2 == INFINITY

    def test_ns_elasticity(self):
        result1 = ns_elasticity(Decimal("1"), Decimal("2"), Decimal("1"), Decimal("2"))
        result2 = ns_elasticity(Decimal("1"), Decimal("1"), Decimal("4"), Decimal("2"))

        assert result1 == Decimal("1")
        assert result2 == Decimal("0.5")

class NewAlternativeSummaryTest(TestCase):
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

    def test(self):
        assert False