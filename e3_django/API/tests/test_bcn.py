from django.test import TestCase
from API.models.userDefined.bcn import BCN

# Create your tests here.

class BCNTest(TestCase):
	def model_create(self):
		return BCN.objects.create(
			bcnID = 0,
			altID = [0],
			bcnType = "Cost",
			bcnSubType = "Direct",
			bcnName = "BCN 1",
			bcnTag = {},
			initialOcc = 1,
			rvBool = True,
			bcnInvestBool = True,
			bcnLife = 30,
			recurBool = None,
			recurInterval = None,
			recurVarRate = None,
			recurVarValue = {},
			recurEndDate = None,
			valuePerQ = 1,
			quant = 100,
			quantVarRate = None,
			quantVarValue = {},
			quantUnit = None,
			)

	def model_create2(self):
		return BCN.objects.create(
			bcnID = 1,
			altID = [0,1],
			bcnType = "Cost",
			bcnSubType = "Indirect",
			bcnName = "BCN 2",
			bcnTag = "Electricity",
			initialOcc = 1,
			bcnRealBool = True,
			rvBool = False,
			bcnInvestBool = False,
			bcnLife = None,
			recurBool = True,
			recurInterval = 1,
			recurVarRate = "percDelta",
			recurVarValue = 0.03,
			recurEndDate = {},
			valuePerQ = 0.087,
			quant = 1000,
			quantVarRate = "percDelta",
			quantVarValue = 0.05,
			quantUnit = "kWh",
			)

	def test_model_create(self):
		created = self.model_create()
		self.assertTrue(isinstance(created, BCN))
		print("\nNew BCN object was created.")

		created2 = self.model_create2()
		self.assertTrue(isinstance(created2, BCN))
		print("New BCN object was created.")

		print("> Passed BCN tests!")
