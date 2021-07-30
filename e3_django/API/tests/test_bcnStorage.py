from django.test import TestCase
from API.models import BCNStorage
from datetime import datetime

"""
BCNStorage tests here using django test.

TODO: read contents of txt file in Unit Tests directory, pass it in
"""

class BCNStorageTest(TestCase):
    def test(self, text):
        # try create object with text
        return
    
    def create_model(self):
        """
        Tests bcnStorageObject1
        """
        res = BCNStorage.objects.create(
            bcnID = 0,
            bcnName = "Cost 1",
            altID = {0},
            bcnType = "Cost",
            bcnSubType = "Direct",
            tag = "Tag 1",
            bcnNonDiscFlow = [0, 200, 0, 0, 0, 0, 0, 0, 0, 0, -73.33333333],
            bcnDiscFlow = [0, 194.1747573, 0, 0, 0, 0, 0, 0, 0, 0, -54.56688709],
            quantList = [0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            quantUnits = "m^3",
            sensBool = False,
            sensFlowNonDisc = None,
            sensFlowDisc = None,
            sensQuantList = None,
            uncBool = False,
            uncFlowNonDisc = None,
            uncFlowDisc = None,
            uncQuantList = None
            )

        print("BCNStorage Type: ", res.bcnType)
        #res.validateBCNStorageObject()

        return res


    def create_model_2(self):
        """
        Tests bcnStorageObject4
        """
        res = BCNStorage.objects.create(
            bcnID = 3,
            bcnName = "Benefit 1",
            altID = [1],
            bcnType = "Benefit",
            bcnSubType = "Direct",
            tag = "Tag 1",
            bcnNonDiscFlow = [0, 0, 30.603, 0, 31.8393612, 0, 31.83617726, 0, 32.79762982, 0, 32.14167722],
            bcnDiscFlow = [0, 0, 28.84626261, 0, 28.28886004, 0, 26.66229725, 0, 25.89075184, 0, 23.91642643],
            quantList = [0, 0, 30.603, 0, 31.8393612, 0, 31.83617726, 0, 32.79762982, 0, 32.14167722],
            quantUnits = "m^3",
            sensBool = False,
            sensFlowNonDisc = None,
            sensFlowDisc = None,
            sensQuantList = None,
            uncBool = False,
            uncFlowNonDisc = None,
            uncFlowDisc = None,
            uncQuantList = None
            )

        return res


    def create_model_3(self):
        """
        Tests bcnStorageObject9
        """
        res = BCNStorage.objects.create(
            bcnID = 8,
            bcnName = "NM 1",
            altID = [1, 2],
            bcnType = "Non-Monetary",
            bcnSubType = "Direct",
            tag = "Tag 3",
            bcnNonDiscFlow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            bcnDiscFlow = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            quantList = [100, 100, 100, 100, 100, 100, 100, 100, 100, 100, 100],
            quantUnits = "m",
            sensBool = False,
            sensFlowNonDisc = None,
            sensFlowDisc = None,
            sensQuantList = None,
            uncBool = False,
            uncFlowNonDisc = None,
            uncFlowDisc = None,
            uncQuantList = None
            )

        return res

    def test_create_model(self):
        created = [self.create_model(), self.create_model_2, self.create_model_3]
        for x in created:
            self.assertTrue(isinstance(x, BCNStorage()))

        print("\nNew BCNStorage object(s) were created.")
        print(">>> Passed Analysis tests!")