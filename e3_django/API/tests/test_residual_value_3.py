from unittest import TestCase
from datetime import datetime
import logging
from decimal import Decimal
import os
import sys
from pprint import pprint

from API.objects import Alternative, Analysis, Bcn, Sensitivity, Input, Edges
from API.tasks import analyze
from API.serializers import SensitivitySerializer
# from django.core.exceptions import ValidationError

"""
Sensitivity tests
"""
logger = logging.getLogger(__name__)

class SensitivityTest(TestCase):
    def setUp(self):
        self.analysis = Analysis(
            analysisType="LCCA",
            projectType="Buildings",
            objToReport=["FlowSummary", "MeasureSummary", "OptionalSummary"],
            studyPeriod=40,
            baseDate=datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
            serviceDate=datetime.strptime('2013-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
            timestepVal="Year",
            timestepComp="EndOfYear",
            outputRealBool=True,
            interestRate=0.03,
            dRateReal=0.03,
            dRateNom=None,
            inflationRate=0.022,
            Marr=0.03,
            reinvestRate=0.03,
            incomeRateFed=0.26,
            incomeRateOther=0.26,
            location=["", "", "", "", "", "", "20910", ""],
            noAlt=7,
            baseAlt=0,
        )
        self.alternative1 = Alternative(
            altID=0,
            altName="Zero Baseline",
            altBCNList=[0],
            baselineBool=True,
        )
        self.alternative2 = Alternative(
            altID=1,
            altName="Non-Recurring t_0-0 l_0 = h",
            altBCNList=[1],
            baselineBool=False,
        )
        self.alternative3 = Alternative(
            altID=2,
            altName="Non-Recurring t_0-1 l_0 = h",
            altBCNList=[2],
            baselineBool=False,
        )
        self.alternative4 = Alternative(
            altID=3,
            altName="Non-Recurring t_0-2 l_0 = h",
            altBCNList=[3],
            baselineBool=False,
        )
        self.alternative5 = Alternative(
            altID=4,
            altName="Non-Recurring t_0-0 l_0 = h + 5",
            altBCNList=[4],
            baselineBool=False,
        )
        self.alternative6 = Alternative(
            altID=5,
            altName="Non-Recurring t_0-1 l_0 = h + 5",
            altBCNList=[5],
            baselineBool=False,
        )
        self.alternative7 = Alternative(
            altID=6,
            altName="Non-Recurring t_0-2 l_0 = h + 5",
            altBCNList=[6],
            baselineBool=False,
        )
        self.bcn0 = Bcn(
            bcnID=0,
            altID=[0],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="Zero Baseline",
            bcnTag=None,
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=True,
            rvOnly=False,
            bcnLife=7,
            recurBool=True,
            recurInterval=5,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=0,
            quant=Decimal(100),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=40,
        )
        self.bcn1 = Bcn(
            bcnID=1,
            altID=[1],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="No Residual Value 1",
            bcnTag=None,
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=True,
            rvOnly=False,
            bcnLife=5,
            recurBool=True,
            recurInterval=5,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=Decimal(100),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=40,
        )
        self.bcn2 = Bcn(
            bcnID=2,
            altID=[2],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="No Residual Value 2",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=True,
            rvOnly=False,
            bcnLife=5,
            recurBool=True,
            recurInterval=5,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=Decimal(100),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=40,
        )
        self.bcn3 = Bcn(
            bcnID=3,
            altID=[3],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="Residual Value 1 div 5",
            bcnTag=None,
            initialOcc=2,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=True,
            rvOnly=True,
            bcnLife=5,
            recurBool=True,
            recurInterval=5,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=Decimal(100),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=40,
        )
        self.bcn4 = Bcn(
            bcnID=4,
            altID=[4],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="Residual Value 5 div 10 one",
            bcnTag=None,
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=True,
            rvOnly=False,
            bcnLife=10,
            recurBool=True,
            recurInterval=10,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=Decimal(100),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=40,
        )
        self.bcn5 = Bcn(
            bcnID=5,
            altID=[5],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="Residual Value 5 div 10 two",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=True,
            rvOnly=False,
            bcnLife=10,
            recurBool=True,
            recurInterval=10,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=Decimal(100),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=40,
        )
        self.bcn6 = Bcn(
            bcnID=6,
            altID=[6],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="Residual Value 6 div 10",
            bcnTag=None,
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=True,
            rvOnly=False,
            bcnLife=1,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=Decimal(100),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=40,
        )

        logger.info("Success!: %s", "Setup tests passed.")

        return

    def test_output_accuracy(self):
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'e3_django.settings')
        try:
            from django.core.management import execute_from_command_line
        except ImportError as exc:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            ) from exc
        execute_from_command_line(sys.argv)

        self.sensitivityObjects = []
        self.analysisObject = self.analysis
        self.bcnObjects = [self.bcn0, self.bcn1, self.bcn2, self.bcn3, self.bcn4, self.bcn5, self.bcn6] #self.bcn7,
                           #self.bcn8, self.bcn9, self.bcn10, self.bcn11, self.bcn12, self.bcn13, self.bcn14,
                           #self.bcn15, self.bcn16]
        self.alternativeObjects = [self.alternative1, self.alternative2, self.alternative3, self.alternative4
                                   , self.alternative5, self.alternative6, self.alternative7]
        self.edgesObject = None

        analysisData = vars(self.analysisObject)

        bcnData = []
        for i in range(len(self.bcnObjects)):
            bcnData.append(vars(self.bcnObjects[i]))

        alternativeData = []
        for i in range(len(self.alternativeObjects)):
            alternativeData.append(vars(self.alternativeObjects[i]))

        if self.sensitivityObjects:
            sensitivityData = []
            for i in range(len(self.sensitivityObjects)):
                sensitivityData.append(vars(self.sensitivityObjects[i]))
        else:
            sensitivityData = None

        if self.edgesObject:
            edgesData = vars(self.edgesObject)
        else:
            edgesData = None

        inputData = {"analysisObject": analysisData,
                     "bcnObjects": bcnData,
                     "alternativeObjects": alternativeData,
                     "sensitivityObjects": sensitivityData,
                     "edgesObject": edgesData}

        self.input = Input(
            sensitivityObjects=self.sensitivityObjects,
            analysisObject=self.analysisObject,
            bcnObjects=self.bcnObjects,
            alternativeObjects=self.alternativeObjects,
            edgesObject=self.edgesObject,
            scenarioObject=None
        )

        results = analyze(self.input)
