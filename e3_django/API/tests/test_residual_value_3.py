from unittest import TestCase
from datetime import datetime
import logging
from decimal import Decimal
from pprint import pprint

from API.objects import Alternative, Analysis, Bcn, Sensitivity
from API.serializers import SensitivitySerializer
from compute.sensitivity.accuracyTestTemp import run, runCF
from compute.required.apps import calculate_required_flows
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
        self.sensitivityObjects = []
        self.analysisObject = self.analysis
        self.bcnObjects = [self.bcn0, self.bcn1, self.bcn2, self.bcn3, self.bcn4, self.bcn5, self.bcn6] #self.bcn7,
                           #self.bcn8, self.bcn9, self.bcn10, self.bcn11, self.bcn12, self.bcn13, self.bcn14,
                           #self.bcn15, self.bcn16]
        self.alternativeObjects = [self.alternative1, self.alternative2, self.alternative3, self.alternative4
                                   , self.alternative5, self.alternative6, self.alternative7]

        self.base_input = BaseInput(
            sensitivityObjects=self.sensitivityObjects,
            analysisObject=self.analysisObject,
            bcnObjects=self.bcnObjects,
            alternativeObjects=self.alternativeObjects,
        )
        timestep_comp = self.analysis.timestepComp
        studyPeriod = self.analysis.studyPeriod
        cash_flow = runCF(self.base_input, timestep_comp)

        reqFlows = calculate_required_flows(cash_flow.keys(), studyPeriod, cash_flow)

        for item in reqFlows:
            print(item)