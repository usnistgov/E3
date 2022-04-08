from rest_framework.fields import IntegerField, DictField, CharField, BooleanField
from rest_framework.serializers import Serializer

from API.serializers.fields import InfinityDecimalField
from API.variables import MAX_DIGITS, DECIMAL_PLACES


class SensitivitySummarySerializer(Serializer):
    """
    Object serializer for sensitivity summary.
    """
    globalVarBool = BooleanField(required=False)
    bcnObj = CharField(required=True, allow_null=True)
    varName = CharField(required=True, allow_null=True)
    diffType = CharField(required=True)
    diffVal = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    diffSign = IntegerField(required=True)
    ## altOutput = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    totalBenefits = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    totalCosts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    totalCostsInv = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    totalCostsNonInv = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    totSubtypeFlows = DictField(child=DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)))
    totTagFlows = DictField(child=DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)))
    netBenefits = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    netSavings = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    SIR = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    IRR = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    AIRR = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    DPP = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    SPP = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    BCR = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    quantSum = DictField(child=DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)))
    quantUnits = DictField(child=DictField(child=CharField()))
    MARR = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    deltaQuant = DictField(child=DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)))
    nsDeltaQuant = DictField(child=DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)))
    nsPercQuant = DictField(child=DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)))
    nsElasticityQuant = DictField(child=DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)))
