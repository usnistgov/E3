from unittest import TestCase
from datetime import datetime
import logging
from decimal import Decimal
from pprint import pprint

from API.objects import Alternative, Analysis, Bcn, Sensitivity
from API.serializers import SensitivitySerializer
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
        self.sensitivityObjects = [self.sensitivity1]
        self.analysisObject = self.analysis
        self.bcnObjects = [self.bcn0, self.bcn1, self.bcn2, self.bcn3]
        self.alternativeObjects = [self.alternative1, self.alternative2]

        self.base_input = BaseInput(
            sensitivityObjects=self.sensitivityObjects,
            analysisObject=self.analysisObject,
            bcnObjects=self.bcnObjects,
            alternativeObjects=self.alternativeObjects,
        )
        timestep_comp = self.analysis.timestepComp
        cash_flow = runCF(self.base_input, timestep_comp)

        res = run(self.base_input, cash_flow)
        for sens in res:
            print(sens)

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
