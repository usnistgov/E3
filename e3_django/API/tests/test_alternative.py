from django.test import TestCase
from API.models.userDefined.alternative import Alternative

# Create your tests here.

class AlternativeTest(TestCase):
	def model_create(self):
		return Alternative.objects.create(
			altID = 0,
			altName = "Alternative 1",
			altBCNList = [0,1],
			baselineBool = True,
			)

	def model_create2(self):
		return Alternative.objects.create(
			altID = 1,
			altName = "Alternative 2",
			altBCNList = [1],
			baselineBool = False,
			)

	def test_model_create(self):
		created = self.model_create()
		self.assertTrue(isinstance(created, Alternative))
		print("\nNew Alternative object was created.")

		created2 = self.model_create2()
		self.assertTrue(isinstance(created2, Alternative))
		print("New Alternative object was created.")
		print(">>> Passed Alternative tests!\n")
