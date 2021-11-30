from unittest import TestCase
from datetime import datetime
from decimal import Decimal

from API.objects import Alternative, Analysis, Bcn, Sensitivity

"""
Sensitivity tests
"""

class SensitivityTest(TestCase):
    def setup(self):
        self.alternative = Alternative(
			altID = 0,
			altName = "Alternative 0",
			altBCNList = [0, 1],
			baselineBool = False,
		)
        self.bcn = Bcn(
            bcnID=0,
            altID=[0],
            bcnType="Cost",
            bcnTag=None,
            bcnSubType="Direct",
            bcnName="BCN 1",
            initialOcc=1,
            bcnLife=30,
            bcnRealBool=False,
            bcnInvestBool=True,
            rvBool=True,
            rvOnly=False,
            recurBool=False,
            recurInterval=None,
            recurVarRate=None,
            recurVarValue=None,
            recurEndDate=None,
            valuePerQ=Decimal("2"),
            quant=Decimal("100"),
            quantVarRate=None,
            quantVarValue=None,
            quantUnit=None,
        )
        # standard Analysis object that can be created
        self.analysis = Analysis(
            analysisType="LCCA",
            projectType="Buildings",
            objToReport=["FlowSummary"],
            studyPeriod=10,
            baseDate=datetime.strptime('2012-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
            serviceDate=datetime.strptime('2013-04-23T18:25:43.511Z', '%Y-%m-%dT%H:%M:%S.511Z'),
            timestepVal="Year",
            timestepComp=1,
            outputRealBool=False,
            interestRate=Decimal("0.03"),
            dRateReal=Decimal("0.03"),
            dRateNom=Decimal("0.05"),
            inflationRate=Decimal("0.02"),
            Marr=None,
            reinvestRate=Decimal("0.05"),
            incomeRateFed=None,
            incomeRateOther=None,
            location=["United States", "", "", "Maryland", "", "", "20879", ""],
        )

    def single_sensitivity_creation(self):
        self.sensitivity = Sensitivity(
            globalVarBool=True,
            altID=0,
            bcnID=0,
            bcnObj=self.bcn,
            varName='valuePerQ',
            diffType='Percent',
            diffValue=2
        )

    def generate_sensitivity_summary(self):
        pass