from django.test import TestCase
from decimal import Decimal
from unittest import TestCase
#from datetime import datetime

from API.objects import Alternative

"""
Alternative tests
"""
PLACES = Decimal(10) ** -4

class AlternativeTest(TestCase):
	def setup(self):
		self.alternative0 = Alternative(
			altID = 0,
			altName = "Alternative 0",
			altBCNList = [0, 1],
			baselineBool = False,
		)

		self.alternative1 = Alternative(
			altID = 1,
			altName = "Alternative 1",
			altBCNList = [1],
			baselineBool = False,
		)

	def test_invalid_bcn_id(self):
		"""
		Checks Alternative serializer throws validation error when
		list of bcn IDs associated with altID (altBCNList) does not 
		reference existing BCN object(s).
		"""
		with self.assertRaises(ValidationError):
			self.alternative15 = Alternative(
			altID = 15,
			altName = "Alternative 15",
			altBCNList = [2, 3, 5],
			baselineBool = False,
			)

		with self.assertRaies(ValidationError):
			self.alternative15 = Alternative(
			altID = 16,
			altName = "Alternative 16",
			altBCNList = [-10],
			baselineBool = False,
			)

	def test_validate_baseline_bool(self):
		"""
		Checks that only one alternative can have baselineBool = True.
		"""
		self.alternative2 = Alternative(
			altID = 2,
			altName = "Alternative 2",
			altBCNList = [1, 0],
			baselineBool = False,
		)

		self.alternative3 = Alternative(
			altID = 3,
			altName = "Alternative 3",
			altBCNList = [1],
			baselineBool = False,
		)

		self.alternative4 = Alternative( # First alternative object with baselineBool.
			altID = 4,
			altName = "Alternative 4",
			altBCNList = [0],
			baselineBool = True,
		)

		
		with self.assertRaises(ValidationError): # Check only one alternative can have baselineBool
			self.alternative5 = Alternative(
				altID = 5,
				altName = "Alternative 5",
				altBCNList = [1],
				baselineBool = True,
			)
			self.alternative6 = Alternative(
				altID = 6,
				altName = "Alternative 6",
				altBCNList = [0,1],
				baselineBool = True,
			)

			self.alternative7 = Alternative(
				altID = 7,
				altName = "Alternative 7",
				altBCNList = [1],
				baselineBool = True,
			)

	def test_required_fields(self):
		"""
		Checks all required fields in Alternative object.
		If any of required fields are not provided, cannot create object
		"""
		with self.assertRaises(Exception):
			self.alternative7 = Alternative( # Missing altID
					altID = None,
					altBCNList = [1],
					baselineBool = False,
			)
		with self.assertRaises(Exception): # Missing altBCNList
			self.alternative7 = Alternative(
					altID = 7,
					baselineBool = False,
			)
	"""
	def test_create_model(self):
		created = [self.create_model(), self.create_model_2()]
		for x in created:
			self.assertTrue(isinstance(x, Alternative))
	"""