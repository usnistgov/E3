from rest_framework.fields import IntegerField, ListField, DecimalField, CharField
from rest_framework.serializers import Serializer

from API.variables import MAX_DIGITS, DECIMAL_PLACES


class RequiredCashFlowSerializer(Serializer):
    """
    Object serializer for required cash flow objects.
    """

    altID = IntegerField(required=True)
    totCostNonDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totCostDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                            required=False)
    totBenefitsNonDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totBenefitsDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totCostsNonDiscInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totCostsDiscInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totBenefitsNonDiscInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                      required=False)
    totBenefitsDiscInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totCostNonDiscNonInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                     required=False)
    totCostDiscNonInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                  required=False)
    totBenefitsNonDiscNonInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                         required=False)
    totBenefitsDiscNonInv = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                      required=False)
    totCostDir = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                           required=False)
    totCostDirDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsDir = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsDirDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totCostInd = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                           required=False)
    totCostIndDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsInd = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsIndDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totCostExt = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                           required=False)
    totCostExtDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsExt = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsExtDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)


class OptionalCashFlowSerializer(Serializer):
    """
    Object serializers for optional cash flow serializers.
    """

    altID = IntegerField(required=True)
    tag = CharField(required=True)
    totTagFlowDisc = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=True)
    totTagQ = ListField(child=DecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                        required=True)
    quantUnits = CharField(required=True)
