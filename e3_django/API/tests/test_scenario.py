from django.test import TestCase
from API.models.userDefined.scenario import Scenario

# Create your tests here.

class ScenarioTest(TestCase):
	def model_create(self):
		return Scenario.objects.create(
			objectVariables = None
			)

	def test_model_create(self):
		created = self.model_create()
		self.assertTrue(isinstance(created, Scenario))
		print("\nNew Scenario object was created.")

		print("> Passed Scenario tests!")
