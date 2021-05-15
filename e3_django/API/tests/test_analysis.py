from django.test import TestCase
from API.models.userDefined.analysis import Analysis
from datetime import datetime

# Create your tests here.

class AnalysisTest(TestCase):
	def model_create(self):
		return Analysis.objects.create(
			analysisType = "LCCA",
			projectType = "Buildings",
			objToReport = None, #{ "FlowSummary", "MeasureSummary" },
			studyPeriod = 10,
			baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			serviceDate = datetime.strptime('2013-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			timestepVal = "Year",
			timestepComp = 1,
			outputRealBool = False,
			interestRate = 0.03,
			dRateReal = 0.0,
			dRateNom = 0.05,
			inflationRate = 0.02,
			Marr = 0.04,
			reinvestRate = 0.05,
			incomeRateFed = None,
			incomeRateOther = None,
			location = None,
			)

	def test_model_create(self):
		created = self.model_create()
		self.assertTrue(isinstance(created, Analysis))
		print("\nNew Analysis object was created.")
		print("> Passed Analysis tests!")