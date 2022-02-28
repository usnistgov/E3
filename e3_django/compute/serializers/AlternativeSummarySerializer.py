from rest_framework.fields import CharField, IntegerField, DictField
from rest_framework.serializers import Serializer

from API.serializers.fields import InfinityDecimalField
from API.variables import MAX_DIGITS, DECIMAL_PLACES


class AlternativeSummarySerializer(Serializer):
    """
    Object serializer for alternative summary.
    """

    altID = IntegerField(required=True)
    totalBenefits = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCosts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCostsInv = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totalCostsNonInv = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    totSubtypeFlows = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    totTagFlows = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    netBenefits = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    netSavings = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    SIR = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    IRR = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=3, required=False, allow_null=True)
    AIRR = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    DPP = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    SPP = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    BCR = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, allow_null=True)
    quantSum = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    quantUnits = DictField(child=CharField())
    MARR = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES)
    deltaQuant = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), allow_null=True)
    nsPercQuant = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), allow_null=True)
    nsDeltaQuant = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), allow_null=True)
    nsElasticityQuant = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), allow_null=True)
