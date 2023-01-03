from rest_framework.fields import IntegerField, DictField, CharField, BooleanField
from rest_framework.serializers import Serializer

from API.serializers.fields import InfinityDecimalField
from API.variables import MAX_DIGITS, DECIMAL_PLACES


class EdgesSensitivitySummarySerializer(Serializer):
    """
    Object serializer for edges summary.
    """
    globalVarBool = BooleanField(required=False)
    bcnObj = CharField(required=True, allow_null=True)
    varName = CharField(required=True, allow_null=True)
    diffType = CharField(required=True)
    diffVal = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    diffSign = IntegerField(required=True)
    totalDirectCosts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True))
    totalIndirectCosts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True))
    omrRecur = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    omrOneTime = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    posExtRecur = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    posExtOneTime = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    negExtRecur = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    negExtOneTime = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    pvBens = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True))
    pvCosts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True))
    pvExts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    respRec = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    dirLossRed = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    indirLossRed = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    fatAvert = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    valFatAvert = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    ndrbRecur = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    ndrbOneTime = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    npvExts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    bcrExts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    irrExts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    roiExts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    nonDisRoiExts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    npvNoExts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    bcrNoExts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    irrNoExts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    roiNoExts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    nonDisRoiNoExts = DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True, allow_null=True))
    otherTags = DictField(child=DictField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), allow_null=True))
