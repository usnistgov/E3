from django.test import TestCase
from API.models.userDefined.sensitivity import Sensitivity

# Create your tests here.

class SensitivityTest(TestCase):
	def model_create(self):
		return Sensitivity.objects.create(
			globalVarBool = True,
			altID = None,
			bcnID = None,
			varName = "discountRate",
			diffType = "percent",
			diffVal = 0.5,
			)

	"""
	def model_create2(self):
		return Sensitivity.objects.create(
			globalVarBool = False, 
			altID = [0,1], # In docs, required to be 'INT'
			bcnID = 1, # In docs, required to be a 'STRING'
			varName = "valuePerQ",
			diffType = "percent",
			diffVal = 1,
			)
	"""

	def test_model_create(self):
		created = self.model_create()
		self.assertTrue(isinstance(created, Sensitivity))
		print("\nNew Sensitivity object was created.")

		#created2 = self.model_create2()
		#self.assertTrue(isinstance(created2, Sensitivity))
		#print("\nNew Sensitivity object was created.")

		print(">>> Passed Sensitivity tests!")
		