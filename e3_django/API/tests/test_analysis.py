from django.test import TestCase
from API.models.userDefined import analysis
from API.models.userDefined.analysis import Analysis
from datetime import datetime

"""
Analysis tests here using django test.
"""

class AnalysisTest(TestCase):
	def create_model(self):
		res = Analysis.objects.create(
			analysisType = "LCCA",
			projectType = "Buildings",
			objToReport = ["FlowSummary", "MeasureSummary"],
			studyPeriod = 10,
			baseDate = datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			serviceDate = datetime.strptime('2013-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
			timestepVal = "Year",
			timestepComp = 1,
			outputRealBool = False,
			interestRate = 0.03,
			dRateReal = None,
			dRateNom = 0.05,
			inflationRate = 0.02,
			Marr = 0.04,
			reinvestRate = 0.05,
			incomeRateFed = None,
			incomeRateOther = None,
			location = ["United States", "", "", "Maryland", "", "", "20879", ""],
			)
		print("Analysis Type: ", res.analysisType)

		#res.validateAnalysisObject()
		
		return res


	def test_create_model(self):
		created = self.create_model()
		self.assertTrue(isinstance(created, Analysis))
		print("\nNew Analysis object was created.")
		print(">>> Passed Analysis tests!")