from django.test import TestCase
from API.models.userDefined.scenario import Scenario

# Create your tests here.

class ScenarioTest(TestCase):
	def create_model(self):
		return Scenario.objects.create(
			objectVariables = None
			)

	def test_create_model(self):
		created = self.create_model()
		self.assertTrue(isinstance(created, Scenario))
		print("\nNew Scenario object was created.")

		print(">>> Passed Scenario tests!")
