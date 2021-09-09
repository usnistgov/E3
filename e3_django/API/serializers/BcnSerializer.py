from drf_compound_fields.fields import ListOrItemField
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, ListField, ChoiceField, CharField, BooleanField, DecimalField, DateField
from rest_framework.serializers import Serializer

from API.variables import MAX_DIGITS, DECIMAL_PLACES
from API.serializers.fields import BooleanOptionField
import logging

logger = logging.getLogger(__name__)


class BCNSerializer(Serializer):
    """
    Object serializer for BCN objects.
    """

    bcnID = IntegerField(min_value=0, required=True)
    altID = ListField(child=IntegerField(min_value=0, required=False), required=True)
    bcnType = ChoiceField(["Benefit", "Cost", "Non-Monetary", "0", "1", "2"], required=True)
    bcnSubType = ChoiceField(["Direct", "Indirect", "Externality", "0", "1", "2"], required=False)
    bcnName = CharField(required=False)
    bcnTag = ListOrItemField(child=CharField(required=False), required=False, allow_null=True)
    initialOcc = IntegerField(min_value=0, required=False)
    bcnRealBool = BooleanOptionField({"Nominal", "0"}, {"Real", "1"}, required=False, default=False)
    bcnInvestBool = BooleanField(required=False)
    bcnLife = IntegerField(min_value=1, required=False, allow_null=True)
    rvBool = BooleanField(required=False)
    recurBool = BooleanField(required=True, allow_null=True)
    recurInterval = IntegerField(min_value=1, required=False, allow_null=True)
    recurVarRate = ChoiceField(["Percent Delta Timestep X-1"], required=False, allow_null=True)
    recurVarValue = ListOrItemField(DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), required=False, allow_null=True)
    recurEndDate = IntegerField(required=False, allow_null=True)
    valuePerQ = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    quant = DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    quantVarRate = ChoiceField(["Percent Delta Timestep X-1"], required=False, allow_null=True)
    quantVarValue = ListOrItemField(DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), required=False, allow_null=True)
    quantUnit = CharField(required=False, default='dollars', allow_null=True)

    def validate(self, data):
        # Check all required inputs are given, based on chosen bcnType.
        if data['bcnType'] == 'Benefit':
            if data['initialOcc'] is None or data['bcnRealBool'] is None or not data['valuePerQ']:
                raise ValidationError(f"You must supply: initialOcc, bcnRealBool, valuePerQ if bcnType: Benefit.")
            if not data['quantUnit']:
                logger.info("quantUnit was not provided. Value will be assumed in dollars.")
        elif data['bcnType'] == 'Cost':
            if data['bcnRealBool'] is None or data['bcnInvestBool'] is None or not data['valuePerQ']:
                raise ValidationError(f"You must supply: bcnRealBool, bcnInvestBool, valuePerQ if bcnType: Cost. "
                                      f"Given:\nbcnRealBool: {data['bcnRealBool']} bcnInvestBool: "
                                      f"{data['bcnInvestBool']} valuePerQ: {data['valuePerQ']}")
            if not data['quantUnit']:
                logger.info("quantUnit was not provided. Value will be assumed in dollars.")
        elif data['bcnType'] == 'NonMonetary':
            if not data['bcnTag'] or not data['quantUnit']:
                raise ValidationError("You must supply: bcnTag, quantUnit if bcnType: NonMonetary.")
        else:
            logger.info("BCN type is unknown. Setting to Default.")

        if data['quantVarRate']:
            if not data['quantVarValue']:
                raise ValidationError("You must supply: quantVarValue if quantVarRate exists.")

        if not data['recurEndDate']:
            logger.info("recurEndDate was not provided. BCN will occur for the entire studyPeriod.")

        if data['quantUnit'] == "":
            logger.warning('Warning: %s', 'The quantity unit supplied is blank.')

        return data
