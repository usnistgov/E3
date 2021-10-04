from decimal import Decimal

MAX_DIGITS = 60
DECIMAL_PLACES = 30

CostType = Decimal
FlowType = tuple[list[CostType], list[CostType], list[CostType]]

VAR_RATE_OPTIONS = ["Percent Delta Timestep X-1", "Year by Year"]
