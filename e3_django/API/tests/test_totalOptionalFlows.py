from django.test import TestCase
from API.models import TotalOptionalFlows

"""
TotalOptionalFlows tests here using django test.
"""

class TotalOptionalFlows(TestCase):
    def create_model(self):
        """
        Tests totalOptionalFlows1
        """
        res = TotalOptionalFlows.objects.create(
            altID = 0,
            sensBool = True,
            uncBool = True,
            bcnType = "Non-Monetary",
            bcnSubtype = "Indirect",
            bcnTag = "Non-Monetary Example",
            totTagFlowDisc = [0, 0, 0, 0, 0, 0],
            totTagQ = [1, 53.64, 23, 63.34, -234.3, 234.1],
            quantUnits = "lbs"
        )
        
        #res.validateTotalOptionalFlows()
        return res

    def create_model_2(self):
        """
        Tests totalOptionalFlows2
        """
        res = TotalOptionalFlows.objects.create(
            altID = 3,
            sensBool = False,
            uncBool = True,
            bcnType = "Cost",
            bcnSubtype = "Externality",
            bcnTag = "Monetary Example",
            totTagFlowDisc = [4.32, 7.475, 14,52.43, 64.34, 23.634],
            totTagQ = [1, 53.64, 23, 63.34, -234.3, 234.1],
            quantUnits = "hrs"
        )

    #TODO: check correct logging

    def test_create_model(self):
        created = [self.create_model(), self.create_model_2()]
        for x in created:
            self.assertTrue(isinstance(x, TotalOptionalFlows))

        print("\nNew TotalOptionalFlows object(s) were created.")
        print(">>> Passed TotalOptionalFlows tests!")