from unittest import TestCase
from datetime import datetime
import logging
from decimal import Decimal
import os
import sys
from pprint import pprint

from API.objects import Alternative, Analysis, Bcn, Sensitivity, Input, Edges
from API.tasks import analyze
from compute.sensitivity.accuracyTestTemp import run, runCF
from base_input import BaseInput
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
            objToReport=["SensitivitySummary", "IRRSummary"],
            studyPeriod=50,
            baseDate=datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
            serviceDate=datetime.strptime('2013-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
            timestepVal="Year",
            timestepComp="Continuous",
            outputRealBool=True,
            interestRate=0.03,
            dRateReal=0.03,
            dRateNom=None,
            inflationRate=0.02,
            Marr=0.04,
            reinvestRate=0.05,
            incomeRateFed=0.26,
            incomeRateOther=0.26,
            location=["UnitedStates", "", "", "Maryland", "", "", "20879", ""],
            noAlt=2,
            baseAlt=0,
        )
        self.alternative1 = Alternative(
            altID=0,
            altName="Retrofit",
            altBCNList=[0, 1, 2, 3, 4, 5],
            baselineBool=True,
        )
        self.alternative2 = Alternative(
            altID=1,
            altName="Levee",
            altBCNList=[6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18],
            baselineBool=False,
        )
        self.bcn0 = Bcn(
            bcnID=0,
            altID=[0],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="RetrofitDirectCost",
            bcnTag=None,
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=None,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=Decimal(3000000),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn1 = Bcn(
            bcnID=1,
            altID=[0],
            bcnType="Cost",
            bcnSubType="Indirect",
            bcnName="RetrofitIndirectCost",
            bcnTag=None,
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=False,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=500000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn2 = Bcn(
            bcnID=2,
            altID=[0],
            bcnType="Benefit",
            bcnSubType="Indirect",
            bcnName="RetrofitIndirectLossReduction",
            bcnTag="DRB",
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=50,
            valuePerQ=1,
            quant=80000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn3 = Bcn(
            bcnID=3,
            altID=[0],
            bcnType="Benefit",
            bcnSubType="Indirect",
            bcnName="RetrofitDirectLossReduction",
            bcnTag="DRB",
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=10400,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn4 = Bcn(
            bcnID=4,
            altID=[0],
            bcnType="Benefit",
            bcnSubType="Direct",
            bcnName="RetrofitResponseAndRecovery",
            bcnTag="DRB",
            initialOcc=1,
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
            valuePerQ=1,
            quant=24000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn5 = Bcn(
            bcnID=5,
            altID=[0],
            bcnType="Benefit",
            bcnSubType="Indirect",
            bcnName="FatalitiesAvertedRetrofit",
            bcnTag="DRB",
            initialOcc=1,
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
            valuePerQ=1,
            quant=30000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn6 = Bcn(
            bcnID=6,
            altID=[1],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="AdditionalRoadworkDirectCost",
            bcnTag=None,
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=None,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=2500000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn7 = Bcn(
            bcnID=7,
            altID=[1],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="BridgeConstructionDirectCost",
            bcnTag=None,
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=False,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=4250000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn8 = Bcn(
            bcnID=8,
            altID=[1],
            bcnType="Cost",
            bcnSubType="Indirect",
            bcnName="AdditionalRoadworkIndirectCost",
            bcnTag=None,
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=None,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=120000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn9 = Bcn(
            bcnID=9,
            altID=[1],
            bcnType="Cost",
            bcnSubType="Indirect",
            bcnName="BridgeConstructionIndirectCost",
            bcnTag=None,
            initialOcc=0,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=False,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=1,
            quant=175000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn10 = Bcn(
            bcnID=10,
            altID=[1],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="AdditionalRoadworkOMR",
            bcnTag="OMR",
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=50,
            valuePerQ=1,
            quant=3710,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn11 = Bcn(
            bcnID=11,
            altID=[1],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="NewBridgeOMR",
            bcnTag="OMR",
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=50,
            valuePerQ=1,
            quant=25000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn12 = Bcn(
            bcnID=12,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Externality",
            bcnName="GreenhouseGasEmissions",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=50,
            valuePerQ=1,
            quant=77329,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn13 = Bcn(
            bcnID=13,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Externality",
            bcnName="WaterPollution",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=50,
            valuePerQ=1,
            quant=Decimal(39081.0),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn14 = Bcn(
            bcnID=14,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Externality",
            bcnName="WaterPollution",
            bcnTag=None,
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            bcnLife=None,
            recurBool=True,
            rvOnly=False,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=50,
            valuePerQ=1,
            quant=39799,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn15 = Bcn(
            bcnID=15,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Indirect",
            bcnName="NewBridgeIndirectLossReduction",
            bcnTag="DRB",
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=50,
            valuePerQ=1,
            quant=140000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn16 = Bcn(
            bcnID=16,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Direct",
            bcnName="NewBridgeResponseAndRecovery",
            bcnTag="DRB",
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=50,
            valuePerQ=1,
            quant=40000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn17 = Bcn(
            bcnID=17,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Indirect",
            bcnName="FatalitiesAvertedLevee",
            bcnTag="DRB",
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=50,
            valuePerQ=1,
            quant=60000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn18 = Bcn(
            bcnID=18,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Externality",
            bcnName="ReducedCommuteTime",
            bcnTag="NDRB",
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=50,
            valuePerQ=1,
            quant=100000,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.sensitivity1 = Sensitivity(
            globalVarBool=False,
            altID=0,
            bcnID=0,
            bcnObj="RetrofitDirectCost",
            varName='quant',
            diffType='Percent',
            diffValue=0,
        )

        self.sensitivity2 = Sensitivity(
            globalVarBool=False,
            altID=1,
            bcnID=13,
            bcnObj="WaterPollution",
            varName='quant',
            diffType='Percent',
            diffValue=2,
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

        self.sensitivityObjects = [self.sensitivity1, self.sensitivity2]
        self.analysisObject = self.analysis
        self.bcnObjects = [self.bcn0, self.bcn1, self.bcn2, self.bcn3, self.bcn4, self.bcn5, self.bcn6, self.bcn7,
                           self.bcn8, self.bcn9, self.bcn10, self.bcn11, self.bcn12, self.bcn13, self.bcn14, self.bcn15,
                           self.bcn16, self.bcn17, self.bcn18]
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
