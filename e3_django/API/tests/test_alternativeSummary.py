from django.test import TestCase
from API.models import AlternativeSummary

"""
AlternativeSummary tests here using django test.
"""

class AlternativeSummary(TestCase):
    def create_model(self):
        """
        Tests alternativeSummary1
        """
        res = AlternativeSummary.objects.create(
            altID = 1,
            totalBenefits = 139.69,
            totalCosts = 1580.29,
            totalCostsInv = 431.30,
            totalCostsNonInv = 1148.99,
            netBenefits = -301.34,
            netSavings = -336.34,
            SIR = "Not Calculable",
            IRR = None,
            AIRR = "Not Calculable",
            SPP = "Infinity",
            DPP = "Infinity",
            BCR = "Not Calculable",
            quantSum = [807.987767, 1100],
            quantUnits = [["Tag 1", ",^3"], ["Tag 3", "m"]],
            MARR = 0.04,
            deltaQuant = [["Tag 1",707.9877672], ["Tag 3",1100]],
            nsDeltaQuant = [["Tag 1",-0.4750678],["Tag 3",-0.3057656]],
            nsPercQuant = [["Tag 1",-41.627135],["Tag 3","Infinity"]],
            nsElasticityQuant = [["Tag 1",-0.0334636],["Tag 3","Infinity"]]
        )
        #res.validateAlternativeSummaryObjects()
        return res


    def create_model_2(self):
        """
        Tests alternativeSummary2
        """
        res = AlternativeSummary.objects.create(
            altID = 5,
            totalBenefits = -123.64,
            totalCosts = 234.64,
            totalCostsInv = 890.34,
            totalCostsNonInv = 234.23,
            netBenefits = 432.56, 
            netSavings = 234.64,
            SIR = 1.42,
            IRR = 0.043,
            AIRR = 0.234,
            SPP = 3,
            DPP = 4,
            BCR = 1.42,
            quantSum = [-98.02, 231.2],
            quantUnits = [["Tag 1", ",^3"], ["Tag 3", "m"]],
            MARR = 0.04,
            deltaQuant = [["Tag 1",707.9877672], ["Tag 3",1100]],
            nsDeltaQuant = [["Tag 1",0.2334], ["Tag 3",1.2342]],
            nsPercQuant = [["Tag 1",45.342], ["Tag 3",-0.3242]],
            nsElasticityQuant = [["Tag 1",23.534], ["Tag 3",34.2343]]
        )

        return res


    def test_create_model(self):
        created = [self.create_model(), self.create_model_2()]
        for x in created:
            self.assertTrue(isinstance(x, AlternativeSummary()))

        print("\nNew AlternativeSummary object was created.")
        print(">>> Passed AlternativeSummary tests!")