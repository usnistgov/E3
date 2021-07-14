from rest_framework.fields import IntegerField, ListField, DecimalField
from rest_framework.serializers import Serializer

from API.serializers import MAX_DIGITS, DECIMAL_PLACES


class CashFlowSerializer(Serializer):
    altID = IntegerField(required=True)
    totCostDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES), required=False)
    totCostsDiscInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totCostsNonDiscInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totBenefitsDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totCostsDirDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totCostsIndDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totCostsExtDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totBenefitsDirDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totBenefitsIndDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totBenefitsExtDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
