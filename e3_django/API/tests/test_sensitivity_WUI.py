from unittest import TestCase
from datetime import datetime
import logging
from decimal import Decimal
import os
import sys

# from django.core.exceptions import ValidationError
from API.objects import Alternative, Analysis, Bcn, Sensitivity, Input, Edges
from API.tasks import analyze
from API.serializers import EdgesSerializer

"""
Sensitivity tests
"""
logger = logging.getLogger(__name__)


class SensitivityTest(TestCase):
    def setUp(self):
        self.analysis = Analysis(
            analysisType="LCCA",
            projectType="Infrastructure",
            objToReport=["IRRSummary", "EdgesSummary", "EdgesSensitivitySummary"],
            studyPeriod=50,
            baseDate=datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
            serviceDate=datetime.strptime('2013-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
            timestepVal="Year",
            timestepComp="Continuous",
            outputRealBool=True,
            interestRate=0.03,
            dRateReal=0.04,
            dRateNom=None,
            inflationRate=0.02,
            Marr=0.05,
            reinvestRate=0.03,
            incomeRateFed=None,
            incomeRateOther=None,
            location=["UnitedStates", "", "", "Maryland", "", "", "20879", ""],
            noAlt=2,
            baseAlt=0,
        )
        self.alternative1 = Alternative(
            altID=0,
            altName="Base",
            altBCNList=[10],
            baselineBool=True,
        )
        self.alternative2 = Alternative(
            altID=1,
            altName="Mitigation",
            altBCNList=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            baselineBool=False,
        )
        self.edges = Edges(
            mri=25,
            drbList=[3, 4, 5, 6],
            disMag=None,
            vosl=7500000,
            riskPref="Neutral",
            confInt=0.95
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
            recurBool=False,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=6250860,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
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
            bcnInvestBool=True,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=False,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=625086,
            quant=1,
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn2 = Bcn(
            bcnID=2,
            altID=[1],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="Total OMR Costs",
            bcnTag=["OMR", "OMR Recurring"],
            initialOcc=4,
            bcnRealBool=True,
            bcnInvestBool=True,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=4,
            recurVarRate=None,
            recurVarValue=0,
            recurEndDate=50,
            valuePerQ=28430,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn3 = Bcn(
            bcnID=3,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Indirect",
            bcnName="Indirect Loss Reduction",
            bcnTag=["DRB", "Indirect Loss Reduction"],
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
            valuePerQ=588580,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn4 = Bcn(
            bcnID=4,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Direct",
            bcnName="Sludge removal cost",
            bcnTag=["DRB", "Direct Loss Reduction"],
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
            valuePerQ=1700000,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn5 = Bcn(
            bcnID=5,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Direct",
            bcnName="Water Treatment Chemical Cost",
            bcnTag=["DRB", "Direct Loss Reduction"],
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
            valuePerQ=83576,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn6 = Bcn(
            bcnID=6,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Direct",
            bcnName="Reseeding",
            bcnTag=["DRB", "Response and Recovery"],
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
            valuePerQ=180000,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn7 = Bcn(
            bcnID=7,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Indirect",
            bcnName="Recreation Value",
            bcnTag=["NDRB", "NDRB Recurring"],
            initialOcc=1,
            bcnRealBool=True,
            bcnInvestBool=False,
            rvBool=False,
            rvOnly=False,
            bcnLife=None,
            recurBool=True,
            recurInterval=1,
            recurVarRate=None,
            recurVarValue=0,
            recurEndDate=50,
            valuePerQ=-51850,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn8 = Bcn(
            bcnID=8,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Indirect",
            bcnName="River Health (Salmon)",
            bcnTag=["NDRB", "NDRB One-Time"],
            initialOcc=5,
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
            valuePerQ=4620000,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn9 = Bcn(
            bcnID=9,
            altID=[1],
            bcnType="Benefit",
            bcnSubType="Indirect",
            bcnName="River Health (Watershed)",
            bcnTag=["NDRB", "NDRB One-Time"],
            initialOcc=10,
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
            valuePerQ=3780000,
            quant=Decimal(1),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
            studyPeriod=50,
        )
        self.bcn10 = Bcn(
            bcnID=10,
            altID=[0, 1],
            bcnType="Cost",
            bcnSubType="Direct",
            bcnName="Zero Cost Baseline",
            bcnTag="Baseline Costs",
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
            studyPeriod=50,
        )

        self.sensitivity1 = Sensitivity(
            globalVarBool=True,
            altID=None,
            bcnID=None,
            bcnObj=None,
            varName='discountRate',
            diffType='Percent',
            diffValue=1,
        )

        self.sensitivity2 = Sensitivity(
            globalVarBool=False,
            altID=1,
            bcnID=5,
            bcnObj="Water Treatment Chemical Cost",
            varName='valuePerQ',
            diffType='Gross',
            diffValue=1000,
        )

        self.sensitivity3 = Sensitivity(
            globalVarBool=False,
            altID=1,
            bcnID=6,
            bcnObj="Reseeding",
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

        self.sensitivityObjects = [self.sensitivity1, self.sensitivity2, self.sensitivity3]
        self.analysisObject = self.analysis
        self.bcnObjects = [self.bcn0, self.bcn1, self.bcn2, self.bcn3, self.bcn4, self.bcn5, self.bcn6, self.bcn7,
                           self.bcn8, self.bcn9, self.bcn10]
        self.alternativeObjects = [self.alternative1, self.alternative2]
        self.edgesObject = self.edges

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

        edgesData = vars(self.edgesObject)

        inputData = {"analysisObject": analysisData,
                     "bcnObjects": bcnData,
                     "alternativeObjects": alternativeData,
                     "sensitivityObjects": sensitivityData,
                     "edgesObject": edgesData}

        data = EdgesSerializer(data=inputData)
        data.validate(inputData)

        self.input = Input(
            sensitivityObjects=self.sensitivityObjects,
            analysisObject=self.analysisObject,
            bcnObjects=self.bcnObjects,
            alternativeObjects=self.alternativeObjects,
            edgesObject=self.edgesObject,
            scenarioObject=None
        )

        results = analyze(self.input)
