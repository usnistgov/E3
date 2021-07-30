from decimal import Decimal

from AnalysisSerializer import AnalysisSerializer
from AlternativeSerializer import AlternativeSerializer
from BcnSerializer import BCNSerializer
from CashFlowSerializer import RequiredCashFlowSerializer, OptionalCashFlowSerializer
from SenarioSerializer import ScenarioSerializer
from SensitivitySerializer import SensitivitySerializer

from InputSerializer import InputSerializer
from OutputSerializer import OutputSerializer

MAX_DIGITS = 20
DECIMAL_PLACES = 5

CostType = Decimal
FlowType = tuple[list[CostType], list[CostType], list[CostType]]
