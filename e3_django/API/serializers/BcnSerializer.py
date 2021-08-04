from drf_compound_fields.fields import ListOrItemField
from rest_framework.fields import IntegerField, ListField, ChoiceField, CharField, BooleanField, DecimalField
from rest_framework.serializers import Serializer

from API.variables import MAX_DIGITS, DECIMAL_PLACES
from API.serializers.fields import BooleanOptionField


class BCNSerializer(Serializer):
    bcnID = IntegerField(min_value=0, unique=True, required=True)
    altID = ListField(child=IntegerField(min_value=0, required=False), required=True)
    bcnType = ChoiceField(["Benefit", "Cost", "NonMonetary", "0", "1", "2"], required=True)
    bcnSubType = ChoiceField(["Direct", "Indirect", "Externality", "0", "1", "2"], required=False)
    bcnName = CharField(required=False)
    bcnTag = ListOrItemField(child=CharField(required=False), required=False)
    initialOcc = IntegerField(min_value=0, required=False)
    bcnRealBool = BooleanOptionField({"Nominal", "0"}, {"Real", "1"}, required=False)
    bcnInvestBool = BooleanField(required=False)
    bcnLife = IntegerField(min_value=1, required=False)
    rvBool = BooleanField(required=False)
    recurBool = BooleanField(required=True)
    recurInterval = IntegerField(min_value=1, required=False)
    recurVarRate = ChoiceField(["Percent Delta Timestep X-1"], required=False)
    recurVarValue = ListOrItemField(DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), required=False)
    recurEndDate = DateField(required=False)
    valuePerQ = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    quant = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    quantVarRate = ChoiceField(["Percent Delta Timestep X-1"], required=False)
    quantVarValue = ListOrItemField(DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), required=False)
    quantUnit = CharField(required=False, default='dollars')

    def validate(self, data):
        # Ensure initialOcc occurs at valid timestep

        # Ensure initialOcc is less than studyPeriod
        if data["initialOcc"] >= data["studyPeriod"]:
            raise ValidationError("initialOcc must be less than studyPeriod")
        
        # Ensure recurEndDate is less than studyPeriod
        if data["recurEndDate"] >= data["studyPeriod"]:
            raise ValidationError("recurEndDate must be less than studyPeriod")


        # Check e3_django/API/models/userDefined/bcn.py &
        # Merge to this file:
        
        # 1. Depending on bcnType (Benefit, Cost, NonMonetary), ensure all required inputs are included
        # Else, raise ValidationError

        # 2. Depending on recurBool (True / False), ensure necessary fields are included
        # Else, raise ValidationError

        # 3. If quantVarRate exists, ensure quantVarValue is included
        # Else, raise ValidationError

        return data


    def updateObject(self, varName, newVal):
        self.varName = newVal
        return