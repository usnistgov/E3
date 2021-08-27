import pytest
from google.protobuf.json_format import ParseDict, MessageToDict
from django.test import TestCase

from API.models.userDefined.bcn import BCN
"""
# using pytest (like birdsnest)
@pytest.fixture
def BCN():
	return ParseDict({
		"bcnID": 0,
		"altID": [0],
		"bcnType": "Cost",
		"bcnSubType": "Direct",
		"bcnName": "BCN 1",
		"bcnTag": {},
		"initialOcc": 1,
		"rvBool": True,
		"bcnInvestBool": True,
		"bcnLife": 30,
		"recurBool": {},
		"recurInterval": {},
		"recurVarRate": {},
		"recurVarValue": {},
		"recurEndDate": {},
		"valuePerQ": 1,
		"quant": 100,
		"quantVarRate": {},
		"quantVarValue": {},
		"quantUnit": {}
	}, InputMessage.BCN())


@pytest.mark.django_db
def test_bcn_object(bcn):
	obj = BCN(bcn)
	assert obj.bcnID == 0
	assert obj.altID == [0]

	# test more outputs here
	return 
"""

# using django.test
class BCNTest(TestCase):
	def create_model(self):
		try:
			BCN.objects.create(
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
		except: 
			print("BCN model failed to create")
			return False

	def create_model_2(self):
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
			recurVarRate = "Percent Delta Timestep X-1",
			recurVarValue = 0.03,
			recurEndDate = {},
			valuePerQ = 0.087,
			quant = 1000,
			quantVarRate = "Percent Delta Timestep X-1",
			quantVarValue = 0.05,
			quantUnit = "kWh",
			)

	def test_create_model(self):
		#self.assertFalse(self.model_create())
		print("\nNew BCN object was not created.")

		created = [self.create_model2(), self.create_model()]
		for x in created:
			self.assertTrue(isinstance(x, BCN))

		print("New BCN object(s) were created.")
		print(">>> Passed BCN tests!")
