from unittest import TestCase
from datetime import datetime
import logging
from decimal import Decimal
import os
import sys

from API.objects import Alternative, Analysis, Bcn, Sensitivity, Input
from compute.sensitivity.accuracyTestTemp import run, runCF
from API.tasks import analyze
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
            objToReport=["IRRSummary", "MeasureSummary", "SensitivitySummary"],
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
            quant=Decimal(1),
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
            bcnTag="OMR",
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
            recurVarValue=0,
            recurEndDate=50,
            valuePerQ=23543.2,
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
            bcnName="sludge removal cost",
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
            recurVarValue=0,
            recurEndDate=50,
            valuePerQ=68000,
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
            recurVarValue=0,
            recurEndDate=50,
            valuePerQ=3342.04,
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
            recurVarValue=0,
            recurEndDate=None,
            valuePerQ=7200,
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
            bcnSubType="Externality",
            bcnName=["Ext", "Recreation Value"],
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
            bcnSubType="Externality",
            bcnName=["Ext", "River Health (Salmon)"],
            bcnTag="NDRB",
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
            bcnSubType="Externality",
            bcnName=["Ext", "River Health (Watershed)"],
            bcnTag="NDRB",
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
            diffValue=0,
        )

        self.sensitivity2 = Sensitivity(
            globalVarBool=False,
            altID=1,
            bcnID=9,
            bcnObj="River Health (Watershed)",
            varName='initialOcc',
            diffType='Gross',
            diffValue=0.5,
        )

        self.sensitivity3 = Sensitivity(
            globalVarBool=False,
            altID=1,
            bcnID=9,
            bcnObj="River Health (Watershed)",
            varName='recurInterval',
            diffType='Percent',
            diffValue=50,
        )

        logger.info("Success!: %s", "Setup tests passed.")

        return

    def test_output_accuracy(self):
        self.sensitivityObjects = [self.sensitivity1, self.sensitivity2, self.sensitivity3]
        self.analysisObject = self.analysis
        self.bcnObjects = [self.bcn0, self.bcn1, self.bcn2, self.bcn3, self.bcn4, self.bcn5, self.bcn6, self.bcn7,
                           self.bcn8, self.bcn9, self.bcn10]
        self.alternativeObjects = [self.alternative1, self.alternative2]

        self.input = Input(
            sensitivityObjects=self.sensitivityObjects,
            analysisObject=self.analysisObject,
            bcnObjects=self.bcnObjects,
            alternativeObjects=self.alternativeObjects,
            edgesObject=None,
            scenarioObject=None
        )

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

        results = analyze(self.input)

        # for item in results["EdgesSummary"]:
        #     print(item)

        # timestep_comp = self.analysis.timestepComp
        # cash_flow = runCF(self.base_input, timestep_comp)
        #
        # res = run(self.base_input, cash_flow)
        # for sens in res:
        #     print(sens)

        # data = {
        #         "globalVarBool": True,
        #         "altID": None,
        #         "bcnID": None,
        #         "bcnObj": None,
        #         "varName":"discountRate",
        #         "diffType": "Gross",
        #         "diffValue": 0.03
        #         }
        #
        # SensitivitySerializer.validate(self, data)
