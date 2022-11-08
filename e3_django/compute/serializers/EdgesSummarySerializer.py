from rest_framework.fields import IntegerField, DictField
from rest_framework.serializers import Serializer

from API.serializers.fields import InfinityDecimalField
from API.variables import MAX_DIGITS, DECIMAL_PLACES


class EdgesSummarySerializer(Serializer):
    """
    Object serializer for edges summary.
    """
    altID = IntegerField(required=True)
    totalDirectCosts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    totalIndirectCosts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    omrRecur = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    omrOneTime = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    posExtRecur = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    posExtOneTime = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    negExtRecur = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    negExtOneTime = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    pvBens = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    pvCosts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    pvExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    respRec = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    dirLossRed = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    indirLossRed = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    fatAvert = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    valFatAvert = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    ndrbRecur = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    ndrbOneTime = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    npvExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    bcrExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    irrExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    roiExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    nonDisRoiExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    npvNoExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    bcrNoExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    irrNoExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    roiNoExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    nonDisRoiNoExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True)
    otherTags = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), allow_null=True)
