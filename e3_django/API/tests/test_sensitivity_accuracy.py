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
            projectType="Infrastructure",
            objToReport=["SensitivitySummary", "IRRSummary"],
            studyPeriod=20,
            baseDate=datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
            serviceDate=datetime.strptime('2013-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
            timestepVal="Year",
            timestepComp="EndOfYear",
            outputRealBool=True,
            interestRate=0.03,
            dRateReal=0.009920581544015763095594256630,
            dRateNom=None,
            inflationRate=0.02,
            Marr=0.05,
            reinvestRate=0.02,
            incomeRateFed=None,
            incomeRateOther=None,
            location=["UnitedStates", "", "", "Maryland", "", "", "20879", ""],
            noAlt=2,
            baseAlt=0,
        )
        self.alternative1 = Alternative(
            altID=0,
            altName="Base",
            altBCNList=[3],
            baselineBool=True,
        )
        self.alternative2 = Alternative(
            altID=1,
            altName="Mitigation",
            altBCNList=[0, 1, 2],
            baselineBool=False,
        )
        self.bcn0 = Bcn(
            bcnID=0,
            altID=[1],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="Straw Wattles",
            bcnTag="Initial Investment",
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=10,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=19,
            valuePerQ=10000,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=20,
        )
        self.bcn1 = Bcn(
            bcnID=1,
            altID=[1],
            bcnType="Cost",
            bcnSubType="Indirect",
            bcnName="Indirect Costs",
            bcnTag="Initial Investment",
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1000,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=20,
        )
        self.bcn2 = Bcn(
            bcnID=2,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Direct",
            bcnName="Total OMR Costs",
            bcnTag="OMR",
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=0,
            recurEndDate=20,
            valuePerQ=2000,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=20,
        )

        self.bcn3 = Bcn(
            bcnID=2,
            altID=[0],
            bcnType="Benefit",
            bcnSubType="Direct",
            bcnName="Total OMR Costs",
            bcnTag="OMR",
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=False,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=0,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=20,
        )

        self.sensitivity1 = Sensitivity(
            globalVarBool=True,
            altID=None,
            bcnID=None,
            bcnObj=None,
            varName='discountRate',
            diffType='Percent',
            diffValue=0,
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

        self.sensitivityObjects = [self.sensitivity1]
        self.analysisObject = self.analysis
        self.bcnObjects = [self.bcn0, self.bcn1, self.bcn2, self.bcn3]
        self.alternativeObjects = [self.alternative1, self.alternative2]
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
