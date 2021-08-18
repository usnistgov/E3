from drf_compound_fields.fields import ListOrItemField
from rest_framework.fields import IntegerField, ListField, ChoiceField, CharField, BooleanField, DecimalField
from rest_framework.serializers import Serializer

from API.variables import MAX_DIGITS, DECIMAL_PLACES
from API.serializers.fields import BooleanOptionField
import logging

logger = logging.getLogger(__name__)

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

        # Check all required inputs are given, based on chosen bcnType.
        if data['bcnType'] == 'Benefit':
            if not data['initialOcc'] or not data['bcnRealBool'] or not data['valuePerQ']:
                raise ValidationError("You must supply: initialOcc, bcnRealBool, valuePerQ if bcnType: Benefit.")
            if not data['quantUnit']:
                logger.info("quantUnit was not provided. Value will be assumed in dollars.")

        elif data['bcnType'] == 'Cost':
            if not data['bcnRealBool'] or not data['bcnInvestBool'] or not data['valuePerQ']:
                raise ValidationError("You must supply: bcnRealBool, bcnInvestBool, valuePerQ if bcnType: Cost.")
            if not data['quantUnit']:
                logger.info("quantUnit was not provided. Value will be assumed in dollars.")
        
        elif data['bcnType'] == 'NonMonetary':
            if not data['bcnTag'] or not data['quantUnit']:
                raise ValidationError("You must supply: bcnTag, quantUnit if bcnType: NonMonetary.")

        else:
            logger.info("BCN type is unknown. Setting to Default.")


        if data['recurBool']:
            if not data['recurInterval'] or not data['recurVarRate'] or not data['recurVarValue']:
                raise ValidationError("You must supply: recurInterval, recurVarRate, recurVarValue if recurBool: True.")
        if data['quantVarRate']:
            if not data['quantVarValue']:
                raise ValidationError("You must supply: quantVarValue if quantVarRate exists.")

        if not data['recurEndDate']:
            logger.info("recurEndDate was not provided. BCN will occur for the entire studyPeriod.")

        if data['quantUnit'] == "":
            logger.warning('Warning: %s', 'The quantity unit supplied is blank.', extra=d)

        return data


    def updateObject(self, varName, newVal):
        self.varName = newVal
        
        return