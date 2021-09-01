from django.test import TestCase
from decimal import Decimal
from unittest import TestCase

from API.objects import Analysis
#from API.models.userDefined import analysis
#from API.models.userDefined.analysis import Analysis
from datetime import datetime

"""
Analysis tests 
"""
PLACES = Decimal(10) ** -4

class AnalysisTest(TestCase):
	def setup(self):
		# standard object that can be created
		self.analysis0 = Analysis(
			analysisType = "LCCA",
			projectType = "Buildings",
			objToReport = ["FlowSummary"],
			studyPeriod = 10,
			baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			serviceDate = datetime.strptime('2013-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			timestepVal = "Year",
			timestepComp = 1,
			outputRealBool = False,
			interestRate = Decimal("0.03"),
			dRateReal = Decimal("0.03"),
			dRateNom = Decimal("0.05"),
			inflationRate = Decimal("0.02"),
			Marr = None,
			reinvestRate = Decimal("0.05"),
			incomeRateFed = None,
			incomeRateOther = None,
			location = ["United States", "", "", "Maryland", "", "", "20879", ""],
		)
		
		self.analysis1 = Analysis(
			analysisType = "BCA",
			projectType = "Infrastructure",
			objToReport = ["FlowSummary", "MeasureSummary"],
			studyPeriod = 10,
			baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			serviceDate = datetime.strptime('2013-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			timestepVal = "Year",
			timestepComp = 1,
			outputRealBool = True,
			interestRate = Decimal("0.05"),
			dRateReal = None,
			dRateNom = [],
			inflationRate = Decimal("0.02"),
			Marr = Decimal("0.04"),
			reinvestRate = None,
			incomeRateFed = [],
			incomeRateOther = [],
			location = ["United States", "", "", "Maryland", "", "", "20879", ""]
		)

		self.analysis2 = Analysis(
			analysisType = "Cost-Loss",
			projectType = "Resilience",
			objToReport = ["FlowSummary", "MeasureSummary"],
			studyPeriod = 10,
			baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			serviceDate = None,
			timestepVal = "Year",
			timestepComp = 1,
			outputRealBool = True,
			interestRate = Decimal("0.05"),
			dRateReal = Decimal("0.03"),
			dRateNom = [],
			inflationRate = Decimal("0.02"),
			Marr = Decimal("0.04"),
			reinvestRate = Decimal("0.05"),
			incomeRateFed = [],
			incomeRateOther = [],
			location = ["United States", "", "", "Maryland", "", "", "20879", ""]
		)

		self.analysis3 = Analysis(
			analysisType = "Profit Maximization",
			projectType = "Manufacturing Process",
			objToReport = None,
			studyPeriod = 10,
			baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			serviceDate = datetime.strptime('2013-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			timestepVal = "Year",
			timestepComp = 1,
			outputRealBool = True,
			interestRate = Decimal("0.05"),
			dRateReal = Decimal("0.03"),
			dRateNom = [],
			inflationRate = Decimal("0.02"),
			Marr = Decimal("0.04"),
			reinvestRate = Decimal("0.05"),
			incomeRateFed = [],
			incomeRateOther = [],
			location = ["United States", "", "", "Maryland", "", "", "20879", ""]
		)

		self.analysis4 = Analysis(
			analysisType = "NA",
			projectType = "Unknown",
			objToReport = ["FlowSummary", "MeasureSummary"],
			studyPeriod = 10,
			baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			serviceDate = datetime.strptime('2013-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			timestepVal = "Year",
			timestepComp = 1,
			outputRealBool = True,
			interestRate = Decimal("0.05"),
			dRateReal = Decimal("0.03"),
			dRateNom = [],
			inflationRate = Decimal("0.02"),
			Marr = Decimal("0.04"),
			reinvestRate = Decimal("0.05"),
			incomeRateFed = [],
			incomeRateOther = [],
			location = ["United States", "", "", "Maryland", "", "", "20879", ""]
		)

	def test_correct_analysis_type(self):
		"""
		If analysisType is not one of: 'LCCA', 'BCA', 'Cost-Loss', 'Profit Maximization', 
		should be set to 'Other
		"""
		for x in [self.analysis0, self.analysis1, self.anslysis2, self.analysis3]:
			assert x.analysisType != 'Other'

		assert self.analysis4.analysisType == "Other"

	def test_correct_project_type(self):
		"""
		If projectType is not one of: 'Buildings', 'Infrastructure', 'Resilience', 'Manufacturing Process', 
		should be set to 'Other
		"""
		for x in [self.analysis0, self.analysis1, self.anslysis2, self.analysis3]:
			assert x.projectType != 'Other'
		
		assert self.analysis4.projectType == "Other"

	def test_valid_study_period(self):
		"""
		Check study period is positive, whole digits, and finite value.
		"""
		valid_study_periods = [1, 5, 10, 100]
		for test_value in valid_study_periods:
			temp = Analysis(
				objToReport = ["FlowSummary"],
				studyPeriod = test_value,
				baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
				timestepVal = "Year",
				timestepComp = 1,
				outputRealBool = False,
				dRateReal = Decimal("0.03"),
				Marr = Decimal("0.04"),
				reinvestRate = Decimal("0.05"),
			)
			assert temp
		
		invalid_study_periods = [0, -1, 0.01, float('inf')] # Decimal, negative, inf, or zero values are invalid
		for test_value in invalid_study_periods:
			with self.assertRaises(Exception): 
				temp = Analysis(
					objToReport = ["FlowSummary"],
					studyPeriod = test_value,
					baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
					timestepVal = "Year",
					timestepComp = 1,
					outputRealBool = False,
					dRateReal = Decimal("0.03"),
					Marr = Decimal("0.04"),
					reinvestRate = Decimal("0.05"),
				)
		
	def test_required_fields(self):
		# If any of required fields are not provided, cannot create object
		with self.assertRaises(Exception):  # No object to report provided
				temp = Analysis(
					objToReport = None,
					studyPeriod = test_value,
					baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
					timestepVal = "Year",
					timestepComp = 1,
					outputRealBool = False,
					dRateReal = Decimal("0.03"),
					Marr = Decimal("0.04"),
					reinvestRate = Decimal("0.05"),
				)

		with self.assertRaises(Exception):  # No study period provided
				temp = Analysis(
					objToReport = ["FlowSummary"],
					studyPeriod = None,
					baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
					timestepVal = "Year",
					timestepComp = 1,
					outputRealBool = False,
					dRateReal = Decimal("0.03"),
					Marr = Decimal("0.04"),
					reinvestRate = Decimal("0.05"),
				)

		with self.assertRaises(Exception):  # No base date provided
				temp = Analysis(
					objToReport = ["FlowSummary"],
					studyPeriod = test_value,
					baseDate = None,
					timestepVal = "Year",
					timestepComp = 1,
					outputRealBool = False,
					dRateReal = Decimal("0.01"),
					Marr = Decimal("0.04"),
					reinvestRate = Decimal("0.05"),
				)

		with self.assertRaises(Exception): 
				temp = Analysis(
					objToReport = ["FlowSummary"],
					studyPeriod = test_value,
					baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
					timestepVal = None, #  No timestep value provided
					timestepComp = 1,
					outputRealBool = False,
					dRateReal = Decimal("0.02"),
					Marr = Decimal("0.04"),
					reinvestRate = Decimal("0.05"),
				)

		with self.assertRaises(Exception): 
				temp = Analysis(
					objToReport = ["FlowSummary"],
					studyPeriod = test_value,
					baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
					timestepVal = "Year",
					timestepComp = None, #  No timestep compound provided
					outputRealBool = False,
					dRateReal = Decimal("0.03"),
					Marr = Decimal("0.04"),
					reinvestRate = Decimal("0.05"),
				)

		with self.assertRaises(Exception): 
				temp = Analysis(
					objToReport = ["FlowSummary"],
					studyPeriod = test_value,
					baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
					timestepVal = "Year",
					timestepComp = 1,
					outputRealBool = None,  # No output (nominal or real dollars)  provided
					dRateReal = Decimal("0.04"),
					Marr = Decimal("0.04"),
					reinvestRate = Decimal("0.05"),
				)

		with self.assertRaises(Exception): 
				temp = Analysis(
					objToReport = ["FlowSummary"],
					studyPeriod = test_value,
					baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
					timestepVal = "Year",
					timestepComp = 1,
					outputRealBool = False,
					dRateReal = None, #  No discount rate (nominal or real) provided
					Marr = Decimal("0.04"),
					reinvestRate = Decimal("0.05"),
				)

	def test_autofill_objToReport(self):
		# If no objToReport, fill with defaults
		assert self.analysis3.objToReport == ['FlowSummary', 'MeasureSummary', 'SensitvitySummary', 'UncertaintySummary', 'IRRSummary']

	def test_autofill_no_MARR(self):
		# If no MARR, check that it autofills with discount rate
		assert self.analysis0.MARR 
		assert type(self.analysis0.MARR) == Decimal()

	def test_autofill_reinvestment(self):
		# If no reinvestment Rate, fill with discount rate
		assert self.analysis1.reinvestRate
		assert type(self.analysis1.reinvestRate) == Decimal()

	def test_dollars_discount_rate(self):
		# Check nominal or real dollars with provided discount rate; 
		# If match, move on
		# Else: attempt to calculate
		# If values cannot be calculated, generate error, send back to GUI with error on top of file

	def test_service_date(self):
		# If service date, fill with base date.
		assert self.analysis2.reinvestRate
		assert type(self.analysis2.reinvestRate) == datetime
		assert self.analysis2.reinvestRate == self.analysis2.baseDate

	def test_inflation_rate_calc(self):
		"""
		Checks correct inflation rate is computed from nominal & real discount rates
		a.	If they match, then move on
		b.	If they do not match, then attempt to calculate the missing values and add to the object and save and move on (see formulas in Section 4.4)
		c.	If the values cannot be calculated then generate an error and send the file back to the GUI with the error added to the top of the file.
		"""
		assert calculate_inflation_rate(1, 1) == 0
		assert calculate_inflation_rate(0.1, 0.1) == 0
		assert calculate_inflation_rate(1, 0.1) == 9


	def test_discount_rate_nominal(self):
		"""
		Checks correct inflation rate is computed from nominal & real discount rates
		a.	If they match, then move on
		b.	If they do not match, then attempt to calculate the missing values and add to the object and save and move on (see formulas in Section 4.4)
		c.	If the values cannot be calculated then generate an error and send the file back to the GUI with the error added to the top of the file.
		"""
		assert calculate_discount_rate_nominal(1, 1) == 3
		assert calculate_discount_rate_nominal(0.1, 0.1) == 0.21
		assert calculate_discount_rate_nominal(1.2, 0.1) == 1


	def test_discount_rate_real(self):
		"""
		Checks correct inflation rate is computed from nominal & real discount rates
		a.	If they match, then move on
		b.	If they do not match, then attempt to calculate the missing values and add to the object and save and move on (see formulas in Section 4.4)
		c.	If the values cannot be calculated then generate an error and send the file back to the GUI with the error added to the top of the file.
		"""
		assert calculate_inflation_rate(1, 1) == 0
		assert calculate_inflation_rate(0.1, 0.1) == 0
		assert calculate_inflation_rate(1, 0.1) == 9


	def test_create_model(self):
		created = self.create_model()
		self.assertTrue(isinstance(created, Analysis))