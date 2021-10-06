import pprint
from decimal import Decimal
from unittest import TestCase

import pytest

from API.objects import Bcn
from API.variables import CostType
from compute.objects import OptionalCashFlow, RequiredCashFlow
from compute.objects.AlternativeSummary import sir, bcr, net_savings, net_benefits, check_fraction, airr, \
    payback_period, ns_per_q, ns_per_pct_q, ns_elasticity, calculate_quant_sum, calculate_quant_units, \
    calculate_delta_quant, calculate_ns_perc_quant, calculate_ns_delta_quant, calculate_ns_elasticity_quant, \
    AlternativeSummary

PLACES = Decimal(10) ** -13
SIGNIFICANT = Decimal(10) ** -4

INFINITY = Decimal("Infinity")
NOT_CALCULABLE = CostType("Nan")

DELTA_VAR_RATE = "Percent Delta Timestep X-1"
TAG_1 = "Tag 1"
TAG_3 = "Tag 3"


@pytest.fixture
def bcn_1():
    return Bcn(
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
            recurVarRate=DELTA_VAR_RATE,
            recurVarValue=CostType("0.03"),
            recurEndDate=None,
            valuePerQ=CostType("2"),
            quant=CostType("100"),
            quantVarRate=DELTA_VAR_RATE,
            quantVarValue=CostType("0.05"),
            quantUnit="kWh"
        )


@pytest.fixture
def bcn_2():
    return Bcn(
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
        )


@pytest.fixture
def bcn_3():
    return Bcn(
            10,
            bcnID=3,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Direct",
            bcnName="Benefit 1",
            bcnTag=TAG_1,
            initialOcc=2,
            bcnInvestBool=False,
            rvBool=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=2,
            recurVarRate=DELTA_VAR_RATE,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=CostType("1"),
            quant=CostType("30"),
            quantVarRate=DELTA_VAR_RATE,
            quantVarValue=[0, 0.01, 0.01, 0.02, 0.02, 0.01, -0.01, 0.02, 0.01, 0, -0.02],
            quantUnit="m^3"
        )


@pytest.fixture
def bcn_5():
    return Bcn(
            10,
            bcnID=5,
            altID=[1, 2],
            bcnType="Benefit",
            bcnSubType="Indirect",
            bcnName="Benefit 3",
            bcnTag=TAG_1,
            initialOcc=0,
            bcnInvestBool=False,
            rvBool=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=DELTA_VAR_RATE,
            recurVarValue=CostType("0.01"),
            recurEndDate=7,
            valuePerQ=CostType("0.01"),
            quant=CostType("90"),
            quantVarRate=DELTA_VAR_RATE,
            quantVarValue=CostType("-0.03"),
            quantUnit="m^3"
        )


@pytest.fixture
def bcn_8():
    return Bcn(
            10,
            bcnID=8,
            altID=[1, 2],
            bcnType="Non-Monetary",
            bcnSubType="Direct",
            bcnName="NM 1",
            bcnTag=TAG_3,
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


def test_sir_infinity():
    result = sir(Decimal("431.304392192082"), Decimal("133.831872126668"), Decimal("94.9622352953234"),
                 Decimal("1148.99048312239"))
    assert result.is_infinite()


def test_sir_0():
    result = sir(Decimal("1148.99048"), Decimal("1148.99048"), Decimal("139.60787"), Decimal("0"))
    assert result == 0


def test_sir_not_calculable():
    result = sir(Decimal("431.304392192082"), Decimal("1148.99048312239"), Decimal("94.9622352953234"),
                 Decimal("1148.99048312239"))
    assert result.is_nan()


def test_sir():
    result = sir(Decimal("550"), Decimal("300"), Decimal("200"), Decimal("100"))
    assert result == Decimal("2.5")


def test_bcr_not_calculable():
    result = bcr(Decimal("-301.340592511856"), Decimal("94.9622352953234"), Decimal("431.304392192082"))
    assert result.is_nan()


def test_bcr():
    result = bcr(Decimal("4711.42470789861"), Decimal("431.304392192082"), Decimal("94.9622352953234"))
    assert result.quantize(PLACES) == Decimal("14.0078328312106")


def test_bcr_infinity():
    result = bcr(Decimal("139.607870189127"), Decimal("0"), Decimal("139.607870189127"))
    assert result.is_infinite()


def test_net_savings():
    result1 = net_savings(Decimal("1243.95271841771"), Decimal("1580.29487531447"))
    result2 = net_savings(Decimal("1"), Decimal("0"))
    result3 = net_savings(Decimal("1"), Decimal("1"))

    assert result1.quantize(Decimal(10) ** -7) == Decimal("-336.3421569")
    assert result2 == Decimal("1")
    assert result3 == Decimal("0")


def test_net_benefits():
    result = net_benefits(Decimal("0"), Decimal("1148.99048"), Decimal("0"), Decimal("1288.59835"))
    assert result == Decimal("139.60787")


def test_check_fraction_normal():
    result = check_fraction(Decimal("2"), Decimal("2"))
    assert result == Decimal("1")


def test_check_fraction_infinity():
    result = check_fraction(Decimal("1"), Decimal("-2"))
    assert result.is_infinite()


def test_check_fraction_not_calculable():
    result = check_fraction(Decimal("-1"), Decimal("-2"))
    assert result.is_nan()


def test_airr():
    result = airr(Decimal("1"), Decimal("0.05"), 10)
    assert result == Decimal("0.05")

    result = airr(Decimal("2.5"), Decimal("0.05"), 10)
    assert result.quantize(PLACES) == Decimal("0.150756137704478").quantize(PLACES)


def test_airr_not_calculable():
    result = airr(Decimal("0"), Decimal("0.05"), 10)
    assert result.is_nan()


def test_airr_not_calculable_if_sir_infinity():
    result = airr(INFINITY, Decimal("0.05"), 10)
    assert result.is_nan()


def test_airr_not_calculable_if_sir_not_calculable():
    result = airr(NOT_CALCULABLE, Decimal("0.05"), 10)
    assert result.is_nan()


def test_payback_period_parameters_same_length():
    with pytest.raises(ValueError) as exec_info:
        payback_period([1, 1, 1], [2, 2])

    assert isinstance(exec_info.value, ValueError)


def test_payback_period():
    index = payback_period([2, 2, 2, 0], [1, 1, 1, 1])
    assert index == 3


def test_payback_period_default_is_none():
    index = payback_period([2], [1])
    assert index.is_infinite()


def test_ns_per_q_infinity():
    result1 = ns_per_q(Decimal("0"), Decimal("0"))
    result2 = ns_per_q(Decimal("1"), Decimal("0"))

    assert result1.is_infinite()
    assert result2.is_infinite()


def test_ns_per_q():
    result1 = ns_per_q(Decimal("1"), Decimal("1"))
    result2 = ns_per_q(Decimal("1"), Decimal("2"))

    assert result1 == Decimal("1")
    assert result2 == Decimal("0.5")


def test_ns_per_pct_q_infinity():
    result1 = ns_per_pct_q(Decimal("0"), Decimal("0"), Decimal("0"))
    result2 = ns_per_pct_q(Decimal("1"), Decimal("1"), Decimal("0"))

    assert result1.is_infinite()
    assert result2.is_infinite()


def test_ns_per_pct_q():
    result1 = ns_per_pct_q(Decimal("1"), Decimal("4"), Decimal("2"))
    result2 = ns_per_pct_q(Decimal("1"), Decimal("1"), Decimal("1"))

    assert result1 == Decimal("0.5")
    assert result2 == Decimal("1")


def test_ns_elasticity_infinity():
    result1 = ns_elasticity(Decimal("1"), Decimal("0"), Decimal("1"), Decimal("1"))
    result2 = ns_elasticity(Decimal("1"), Decimal("1"), Decimal("1"), Decimal("0"))

    assert result1.is_infinite()
    assert result2.is_infinite()


def test_ns_elasticity():
    result1 = ns_elasticity(Decimal("1"), Decimal("2"), Decimal("1"), Decimal("2"))
    result2 = ns_elasticity(Decimal("1"), Decimal("1"), Decimal("4"), Decimal("2"))

    assert result1 == Decimal("1")
    assert result2 == Decimal("0.5")


def test_calculate_quant_sum():
    # Given
    x = OptionalCashFlow(0, "tag1", "units", 1).add(None, ([CostType(1)] * 2, [CostType(2)] * 2, [CostType(3)] * 2))
    y = OptionalCashFlow(0, "tag1", "units", 1).add(None, ([CostType(4)] * 2, [CostType(5)] * 2, [CostType(6)] * 2))

    # When
    result = calculate_quant_sum([x, y])

    # Expect
    assert result == [CostType("2"), CostType("8")]


def test_calculate_quant_sum_with_bcns(bcn_1, bcn_2, bcn_3, bcn_5, bcn_8):
    # Given
    optionals = {}

    for bcn in [bcn_1, bcn_2, bcn_3, bcn_5, bcn_8]:
        for tag in bcn.bcnTag:
            if tag is None:
                continue

            if tag not in optionals:
                optionals[tag] = OptionalCashFlow(1, tag, bcn.quantUnit, 10)

            optionals[tag].add(bcn, bcn.cash_flows(10, CostType("0.03")))

    # When
    result = calculate_quant_sum(optionals.values())
    result = [x.quantize(SIGNIFICANT) for x in result]

    # Expect
    assert result == [x.quantize(SIGNIFICANT) for x in [CostType("807.987767188945"), CostType("1100")]]


def test_calculate_quant_units(bcn_1, bcn_2, bcn_3, bcn_5, bcn_8):
    # Given
    optionals = {}

    for bcn in [bcn_1, bcn_2, bcn_3, bcn_5, bcn_8]:
        for tag in bcn.bcnTag:
            if tag is None:
                continue

            if tag not in optionals:
                optionals[tag] = OptionalCashFlow(1, tag, bcn.quantUnit, 10)

            optionals[tag].add(bcn, bcn.cash_flows(10, CostType("0.03")))

    # When
    result = calculate_quant_units(optionals.values())

    # Expect
    assert result == {TAG_1: "m^3", TAG_3: "m"}


def test_calculate_delta_quant(bcn_1, bcn_2, bcn_3, bcn_5, bcn_8):
    # Given
    optionals = {}

    for bcn in [bcn_1, bcn_2, bcn_3, bcn_5, bcn_8]:
        for tag in bcn.bcnTag:
            if tag is None:
                continue

            if tag not in optionals:
                optionals[tag] = OptionalCashFlow(1, tag, bcn.quantUnit, 10)

            optionals[tag].add(bcn, bcn.cash_flows(10, CostType("0.03")))

    # When
    result = calculate_delta_quant(optionals.values(), {TAG_1: CostType("100")})
    result = {k: v.quantize(SIGNIFICANT) for k, v in result.items()}

    # Expect
    assert len(result) == 2
    assert result[TAG_1] == CostType("707.987767188945").quantize(SIGNIFICANT)
    assert result[TAG_3] == CostType("1100").quantize(SIGNIFICANT)


def test_calculate_ns_perc_quant(bcn_1, bcn_2, bcn_3, bcn_5, bcn_8):
    # Given
    optionals = {}

    for bcn in [bcn_1, bcn_2, bcn_3, bcn_5, bcn_8]:
        for tag in bcn.bcnTag:
            if tag is None:
                continue

            if tag not in optionals:
                optionals[tag] = OptionalCashFlow(1, tag, bcn.quantUnit, 10)

            optionals[tag].add(bcn, bcn.cash_flows(10, CostType("0.03")))

    # When
    result = calculate_ns_perc_quant(CostType("-336.342156896759"), optionals.values(), {TAG_1: CostType("100")})

    # Expect
    assert len(result) == 2
    assert result[TAG_1].quantize(SIGNIFICANT) == CostType("-41.6271347853347").quantize(SIGNIFICANT)
    assert result[TAG_3].is_infinite()


def test_calculate_ns_delta_quant(bcn_1, bcn_2, bcn_3, bcn_5, bcn_8):
    # Given
    optionals = {}

    for bcn in [bcn_1, bcn_2, bcn_3, bcn_5, bcn_8]:
        for tag in bcn.bcnTag:
            if tag is None:
                continue

            if tag not in optionals:
                optionals[tag] = OptionalCashFlow(1, tag, bcn.quantUnit, 10)

            optionals[tag].add(bcn, bcn.cash_flows(10, CostType("0.03")))

    # When
    result = calculate_ns_delta_quant(
        CostType("-336.342156896759"),
        calculate_delta_quant(optionals.values(), {TAG_1: CostType("100")}),
        optionals.values()
    )
    result = {k: v.quantize(SIGNIFICANT) if isinstance(v, CostType) else v for k, v in result.items()}

    # Expect
    assert result == {
        TAG_1: CostType("-0.47506775185142").quantize(SIGNIFICANT),
        TAG_3: CostType("-0.305765597178871").quantize(SIGNIFICANT)
    }


def test_calculate_ns_elasticity_quant(bcn_1, bcn_2, bcn_3, bcn_5, bcn_8):
    # Given
    optionals = {}

    for bcn in [bcn_1, bcn_2, bcn_3, bcn_5, bcn_8]:
        for tag in bcn.bcnTag:
            if tag is None:
                continue

            if tag not in optionals:
                optionals[tag] = OptionalCashFlow(1, tag, bcn.quantUnit, 10)

            optionals[tag].add(bcn, bcn.cash_flows(10, CostType("0.03")))

    # When
    result = calculate_ns_elasticity_quant(
        CostType("-336.342156896759"),
        CostType("1243.95271841771"),
        optionals.values(),
        {TAG_1: CostType("100")}
    )

    # Expect
    assert len(result) == 2
    assert result[TAG_1].quantize(SIGNIFICANT) == CostType("-0.033463598872378").quantize(SIGNIFICANT)
    assert result[TAG_3].is_infinite()


class NewAlternativeSummaryTest(TestCase):
    def setUp(self):
        self.bcn0 = Bcn(
            10,
            bcnID=0,
            altID=[0],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="BCN 1",
            bcnTag="test_tag",
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
            quantUnit="test_units"
        )

    def test(self):
        cash_flow = self.bcn0.cash_flows(10, CostType("0.06"))

        required_flow = RequiredCashFlow(0, 10)
        optional_flow = OptionalCashFlow(0, "test_tag", "test_units", 10)

        required_flow.add(self.bcn0, cash_flow)
        optional_flow.add(self.bcn0, cash_flow)

        alternative_summary = AlternativeSummary(0, 0.06, 10, 15, required_flow, [optional_flow], None, False)

        print(alternative_summary.__dict__)

        pp = pprint.PrettyPrinter()
        pp.pprint(alternative_summary.__dict__)
