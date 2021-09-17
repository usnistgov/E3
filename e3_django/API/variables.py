from decimal import Decimal

MAX_DIGITS = 40
DECIMAL_PLACES = 20

CostType = Decimal
FlowType = tuple[list[CostType], list[CostType], list[CostType]]
