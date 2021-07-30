from django.test import TestCase
from API.models import TotalRequiredFlows

"""
TotalRequired tests here using django test.
"""

class TotalRequiredFlows(TestCase):
    def create_model(self):
        """
        Tests totalRequiredFlows1
        """
        res = TotalRequiredFlows.objects.create(
            baselineBool = False,
            sensBool = False,
            uncBool = False,
            totCostNonDisc  = [50, 0, 0, 0, 52.0302005, 500, 0, 0, 54.14283528, 0, -6.903888284],
            totCostDisc  = [50, 0, 0, 0, 46.22815924, 431.3043922, 0, 0, 42.74085414, 0, -5.137141261],
            totCostNonDiscInv  = [0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0],
            totCostDiscInv  = [0, 0, 0, 0, 0, 431.3043922, 0, 0, 0, 0, 0],
            totCostNonDiscNonInv  = [50, 0, 0, 0, 52.0302005, 0, 0, 0, 54.14283528, 0, -6.903888284],
            totCostDiscNonInv  = [50, 0, 0, 0, 46.22815924, 0, 0, 0, 42.74085414, 0, -5.137141261],
            totBenefitsNonDisc  = [0.9, 0.88173, 0.863830881, 1172.049055, 1183.743903, 1148.239628, 1217.06878, 0.779640275, 0, 0, 0],
            totBenefitsDisc  = [0.9, 0.856048544, 0.814243455, 1072.590917, 1051.741126, 990.4815899, 1019.275942, 0.633918889, 0, 0, 0],
            totCostDir  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            totCostInd  = [50, 0, 0, 0, 52.0302005, 0, 0, 0, 54.14283528, 0, -6.903888284],
            totCostExt  = [0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0],
            totCostDirDisc  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            totCostIndDisc  = [50, 0, 0, 0, 46.22815924, 0, 0, 0, 42.74085414, 0, -5.137141261],
            totCostExtDisc  = [0, 0, 0, 0, 0, 431.3043922, 0, 0, 0, 0, 0],
            totBenefitsDir  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            totBenefitsInd  = [0.9, 0.88173, 0.863830881, 1172.049055, 1183.743903, 1148.239628, 1217.06878, 0.779640275, 0, 0, 0],
            totBenefitsExt  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            totBenefitsDirDisc  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            totBenefitsIndDisc  = [0.9, 0.856048544, 0.814243455, 1072.590917, 1051.741126, 990.4815899, 1019.275942, 0.633918889, 0, 0, 0],
            totBenefitsExtDisc  = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        )

        #res.validateTotalRequiredFlows()
        
        return res

    def create_model_2(self):
        """
        Tests totalRequiredFlows2
        """
        res = TotalRequiredFlows.objects.create(
            baselineBool = True,
            sensBool = True,
            uncBool = True,
            totCostNonDisc  = [50, 0, 0, 0, 52.0302005, 500, 0, 0, 54.14283528, 0, -6.903888284],
            totCostDisc  = [50, 0, 0, 0, 46.22815924, 431.3043922, 0, 0, 42.74085414, 0, -5.137141261],
            totCostNonDiscInv  = [0, 0, 0, 0, 0, 500, 0, 0, 0, 0, 0],
            totCostDiscInv  = [0, 0, 0, 0, 0, 431.3043922, 0, 0, 0, 0, 0],
            totCostNonDiscNonInv  = [50, 0, 0, 0, 52.0302005, 0, 0, 0, 54.14283528, 0, -6.903888284],
            totCostDiscNonInv  = [50, 0, 0, 0, 46.22815924, 0, 0, 0, 42.74085414, 0, -5.137141261],
            totBenefitsNonDisc  = [0.9, 0.88173, 0.863830881, 1172.049055, 1183.743903, 1148.239628, 1217.06878, 0.779640275, 0, 0, 0],
            totBenefitsDisc  = [0.9, 0.856048544, 0.814243455, 1072.590917, 1051.741126, 990.4815899, 1019.275942, 0.633918889, 0, 0, 0],
            totCostDir  = [12, 24, 35, 85, 14, 18, 70.23, 63, 25, 85, 365],
            totCostInd  = [50, 0, 0, 0, 52.0302005, 0, 0, 0, 54.14283528, 0, -6.903888284],
            totCostExt  = [13, 52, 123, 23, 78, 500, 79.763, 96, 56, 46, 35],
            totCostDirDisc  = [5, 26, 47, 38, 26, 849, 36.242,253.3, 12.2, 52.7, 532.2],
            totCostIndDisc  = [50, 0, 0, 0, 46.22815924, 0, 0, 0, 42.74085414, 0, -5.137141261],
            totCostExtDisc  = [0, 0, 0, 0, 0, 431.3043922, 0, 0, 0, 0, 0],
            totBenefitsDir  = [345.3, 0, 0, 52, 0, 0, 0, 0, 73, 0, 0],
            totBenefitsInd  = [0.9, 0.88173, 0.863830881, 1172.049055, 1183.743903, 1148.239628, 1217.06878, 0.779640275, 0, 0, 0],
            totBenefitsExt  = [374, 0, 0, 0, 0, 6453.2, 0, 0, 0, 0, 63],
            totBenefitsDirDisc  = [234.32, 0, 0, 0, 42.3, 0, 0, 0, 0, 523.23, 0],
            totBenefitsIndDisc  = [0.9, 0.856048544, 0.814243455, 1072.590917, 1051.741126, 990.4815899, 1019.275942, 0.633918889, 0, 0, 0],
            totBenefitsExtDisc  = [624, 0, 0, 0, 0, 0, 253.234, 0, 0, 0, 234.4]
        )        
        return res

    def test_create_model(self):
        created = [self.create_model(), self.create_model_2()]
        for x in created:
            self.assertTrue(isinstance(x, TotalRequiredFlows()))

        print("\nNew TotalRequiredFlows object(s) were created.")
        print(">>>Passed TotalRequired tests!")