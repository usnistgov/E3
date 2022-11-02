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
    omrRecur = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    omrOneTime = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    posExtRecur = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    posExtOneTime = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    negExtRecur = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    negExtOneTime = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    pvBens = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    pvCosts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    pvExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    respRec = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    dirLossRed = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    indirLossRed = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    fatAvert = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    valFatAvert = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    ndrbRecur = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    ndrbOneTime = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    npvExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    bcrExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    irrExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    roiExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    nonDisRoiExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    npvNoExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    bcrNoExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    irrNoExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    roiNoExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    nonDisRoiNoExts = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    otherTags = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
