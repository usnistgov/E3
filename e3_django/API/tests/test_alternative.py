from django.test import TestCase
from API.models.userDefined.alternative import Alternative

# Create your tests here.

class AlternativeTest(TestCase):
	def create_model(self):
		return Alternative.objects.create(
			altID = 0,
			altName = "Alternative 1",
			altBCNList = [0,1],
			baselineBool = True,
			)

	def create_model_2(self):
		return Alternative.objects.create(
			altID = 1,
			altName = "Alternative 2",
			altBCNList = [1],
			baselineBool = False,
			)

	def test_create_model(self):
		created = [self.create_model(), self.create_model_2()]
		for x in created:
			self.assertTrue(isinstance(x, Alternative))

		print("New Alternative object was created.")
		print(">>> Passed Alternative tests!\n")
