from rest_framework.fields import IntegerField, CharField, ListField, BooleanField, DecimalField
from rest_framework.serializers import Serializer

from API.variables import MAX_DIGITS, DECIMAL_PLACES


class BCNStorageSerializer(Serializer):
    bcnID = IntegerField(required=True)
    bcnName = CharField(required=False, default="")
    altID = ListField(unique=True, child=IntegerField())
    bcnType = CharField(required=False)
    bcnSubType = CharField(required=False)
    tag = CharField(default="")
    bcnNonDiscFlow = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    bcnDiscFlow = ListField(child=DecimalField(max_digit=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    quantList = ListField(DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    quantUnits = CharField(required=True, default="")
    sensBool = BooleanField(required=False)
    sensFlowNonDisc = ListField(child=IntegerField())
    sensFlowDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    sensQuantList = ListField(DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    uncBool = BooleanField(required=False)
    uncFlowNonDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    uncFlowDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))
    uncQuantList = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES))

    def validate(self, data):
        # Check bcnType is equivalent to bcn.type for bcnID
        # Check subType is equivalent to bcn.subType for bcnID
        # Check tag is equivalent to bcn.tag for bcnID
        pass
    
    def updateSensFlows(self, data, newSensFlowNonDisc, newSensFlowDisc, newSensFlowQuant): 
        # Updates sensitivity flows 
        data['sensFlowNonDisc'] = newSensFlowNonDisc
        data['sensFlowDisc'] = newSensFlowDisc
        data['sensQuantList'] = newSensFlowQuant

        return data

    def updateUncFlows(self, data, newUncFlowNonDisc, newUncFlowDisc, newUncFlowQuant): 
        # Updates uncertainty flows
        data['uncFlowNonDisc'] = newUncFlowNonDisc
        data['uncFlowDisc'] = newUncFlowDisc
        data['uncQuantList'] = newUncFlowQuant

        return data