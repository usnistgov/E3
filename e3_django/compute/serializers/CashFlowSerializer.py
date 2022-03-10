from rest_framework.fields import IntegerField, ListField, CharField
from rest_framework.serializers import Serializer

from API.serializers.fields import InfinityDecimalField
from API.variables import MAX_DIGITS, DECIMAL_PLACES


class RequiredCashFlowSerializer(Serializer):
    """
    Object serializer for required cash flow objects.
    """

    altID = IntegerField(required=True)
    totCostNonDisc = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totCostDisc = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                            required=False)
    totBenefitsNonDisc = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totBenefitsDisc = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totCostsNonDiscInv = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totCostsDiscInv = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                required=False)
    totBenefitsNonDiscInv = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                      required=False)
    totBenefitsDiscInv = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totCostNonDiscNonInv = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                     required=False)
    totCostDiscNonInv = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                  required=False)
    totBenefitsNonDiscNonInv = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                         required=False)
    totBenefitsDiscNonInv = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                      required=False)
    totCostDir = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                           required=False)
    totCostDirDisc = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsDir = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsDirDisc = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totCostInd = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                           required=False)
    totCostIndDisc = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsInd = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsIndDisc = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)
    totCostExt = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                           required=False)
    totCostExtDisc = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsExt = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=False)
    totBenefitsExtDisc = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                                   required=False)


class OptionalCashFlowSerializer(Serializer):
    """
    Object serializers for optional cash flow serializers.
    """

    altID = IntegerField(required=True)
    tag = CharField(required=True)
    totTagFlowDisc = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                               required=True)
    totTagQ = ListField(child=InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES),
                        required=True)
    quantUnits = CharField(required=True)
