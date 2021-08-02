from drf_compound_fields.fields import ListOrItemField
from rest_framework.fields import IntegerField, ListField, ChoiceField, CharField, BooleanField, DecimalField
from rest_framework.serializers import Serializer

from API.variables import MAX_DIGITS, DECIMAL_PLACES
from API.serializers.fields import BooleanOptionField


class BCNSerializer(Serializer):
    bcnID = IntegerField(min_value=0, required=True)
    altID = ListField(child=IntegerField(min_value=0, required=False), required=False)
    bcnType = ChoiceField(["Benefit", "Cost", "NonMonetary", "0", "1", "2"], required=False)
    bcnSubType = ChoiceField(["Direct", "Indirect", "Externality", "0", "1", "2"], required=False)
    bcnName = CharField(required=False)
    bcnTag = ListOrItemField(child=CharField(required=False), required=False)
    initialOcc = IntegerField(min_value=0, required=False)
    bcnRealBool = BooleanOptionField({"Nominal", "0"}, {"Real", "1"}, required=False)
    bcnInvestBool = BooleanField(required=False)
    bcnLife = IntegerField(min_value=0, required=False)
    rvBool = BooleanField(required=False)
    recurBool = BooleanField(required=False)
    recurInterval = IntegerField(min_value=0, required=False)
    recurVarRate = ChoiceField(["Percent Delta Timestep X-1"], required=False)
    recurVarValue = ListOrItemField(DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), required=False)
    recurEndDate = IntegerField(min_value=0, required=False)
    valuePerQ = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    quant = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    quantVarRate = ChoiceField(["Percent Delta Timestep X-1"], required=False)
    quantVarValue = ListOrItemField(DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), required=False)
    quantUnit = CharField(required=False)
