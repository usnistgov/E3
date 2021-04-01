from django.test import TestCase
from main.models.userDefined.analysis import Analysis

class ModelsTestCase(TestCase):
      def test_create_analysis_object(self):
            """Analysis object is successfully created"""
            print("called")
            analysis = Analysis.objects.create(
              projectType='type1', 
              interestRate=0.25, 
              dRateNom=0.25,
              inflationRate=0.25,
              incomeRateFed=0.25,
              incomeRateOther=0.25,
              #location=[]
              )
            analysis.save()
            self.assertTrue(True)
"""
import pytest

from ..models import analysis
from ..models.analysis import validateAnalysisObject, validateDiscountRate

@pytest
def Analysis():
    return ParseDict({
      "analysisType": '',
      "projType": "",
      "objToReport" : [""], #! Var Type is specified as: List of Strings, but Format says: {FlowSummary, MeasureSummary}, ...  => (o) 'list' or (x) dict?
      "studyPreiod": 1,
      "baseDate": # date,
      "serviceDate": # date,
      "timestepVal": "Year, Quarter Month, Day",
      "timestepComp": 1,
      "outputRealBool": 0,
      "interestRate": 0.0,
      "dRateReal": 0.0,
      "dRateNom": 0.0, #! Format not specified in documentation
      "inflationRate": 0.0,
      "Marr": 0.0,
      "reinvestRate": 0.0,
      "incomeRateFed": 0.0, #! Format: Federal?
      "incomeRateOther": 0.0, #! Format: State/Local
      "noAlt": 1,
      "baseAlt": 1,
      "location": ["Country", "Region", "Division", "State", "County", "City", "ZIP", "address"]
    })
"""
