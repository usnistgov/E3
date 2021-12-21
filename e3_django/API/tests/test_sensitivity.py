from unittest import TestCase
from datetime import datetime
from decimal import Decimal
import logging

from API.objects import Alternative, Analysis, Bcn
from API.objects.Sensitivity import Sensitivity
from django.core.exceptions import ValidationError

"""
Sensitivity tests
"""
logger = logging.getLogger(__name__)

class SensitivityTest(TestCase):
    def setUp(self):
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
            noAlt=1,
            baseAlt=0,
        )
        self.alternative = Alternative(
			altID = 0,
			altName = "Alternative 0",
			altBCNList = [0, 1],
			baselineBool = False,
		)
        self.bcn0 = Bcn(
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
            studyPeriod=10,
        )
        self.bcn1 = Bcn(
            bcnID=1,
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
            studyPeriod=10,
        )
        # standard Analysis object that can be created
        logger.info("Success!: %s", "Setup tests passed.")
        
        return

    def test_create_sensitivity(self):

        self.sensitivity = Sensitivity(
            globalVarBool=True,
            altID=0,
            bcnID=0,
            bcnObj=self.bcn0,
            varName='valuePerQ',
            diffType='Percent',
            diffValue=2,
        )

    def test_invalid_alt_id(self):
        """
        Checks the Sensitivity serializer throws validation error when 
        alternative ID is invalid or of incorrect data type. 
        """
        with self.assertRaises(ValidationError):
            self.sensitivity1 = Sensitivity(
                globalVarBool=True,
                # Null alternative ID
                altID=None,  
                bcnID=0,
                bcnObj=self.bcn0,
                varName='valuePerQ',
                diffType='Percent',
                diffValue=1,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity2 = Sensitivity(
                globalVarBool=True,
                # Negative alternative ID
                altID=-1,  
                bcnID=0,
                bcnObj=self.bcn0,
                varName='valuePerQ',
                diffType='Percent',
                diffValue=1,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity3 = Sensitivity(
                globalVarBool=True,
                # Infinite/decimal alternative ID
                altID=float('inf'), 
                bcnID=0,
                bcnObj=self.bcn0,
                varName='valuePerQ',
                diffType='Percent',
                diffValue=1,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity4 = Sensitivity(
                globalVarBool=True,
                # String type alternative ID
                altID='1', 
                bcnID=0,
                bcnObj=self.bcn0,
                varName='valuePerQ',
                diffType='Percent',
                diffValue=1,
                )
        logger.info("Success!: %s", "Sensitivity-altID tests passed.")
        
        return


    def test_invalid_bcn_id(self):
        """
        Checks the Sensitivity Serializer throws a validation error when 
        BCN ID is invalid or of incorrect data type.
        """
        with self.assertRaises(ValidationError):
            self.sensitivity5 = Sensitivity(
                globalVarBool=False,
                altID=0,
                # Null BCN ID 
                bcnID=None,  
                # Null associated BCN object
                bcnObj=None,  
                varName='valuePerQ',
                diffType='Gross',
                diffValue=100,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity6 = Sensitivity(
                globalVarBool=True,
                altID=0,
                # Negative BCN ID 
                bcnID=-1,  
                # Valid BCN object
                bcnObj=self.bcn0,  
                varName='valuePerQ',
                diffType='Gross',
                diffValue=100,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity7 = Sensitivity(
                globalVarBool=True,
                altID=0,
                 # Infinite/decimal BCN ID 
                bcnID=float('inf'), 
                # Valid BCN object
                bcnObj=self.bcn0,  
                varName='valuePerQ',
                diffType='Gross',
                diffValue=100,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity8 = Sensitivity(
                globalVarBool=False,
                altID=0,
                 # String type BCN ID 
                bcnID='0', 
                # Valid BCN object
                bcnObj=self.bcn0,  
                varName='valuePerQ',
                diffType='Gross',
                diffValue=100,
            )
        # New BCN object with ID 1

        with self.assertRaises(ValidationError):
            self.sensitivity9 = Sensitivity(
                globalVarBool=False,
                altID=0,
                # Valid BCN ID 
                bcnID=0,  
                # Wrong BCN object associated to BCN ID
                bcnObj=self.bcn1,  
                varName='valuePerQ',
                diffType='Gross',
                diffValue=0,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity10 = Sensitivity(
                globalVarBool=False,
                altID=0,
                # Valid BCN ID 
                bcnID=1,  
                # Wrong BCN object associated to BCN ID
                bcnObj=self.bcn0,  
                varName='valuePerQ',
                diffType='Percent',
                diffValue=0,
            )
        logger.info("Success!: %s", "Sensitivity-bcnID tests passed.")

        return


    def test_incorrect_bcn_obj(self):
        """
        Checks the Sensitivity Serializer throws a validation error when 
        BCN Object is invalid or of incorrect data type.
        """
        with self.assertRaises(ValidationError):
            self.sensitivity11 = Sensitivity(
                globalVarBool=False,
                altID=0,
                bcnID=None,
                # Null BCN object
                bcnObj=None,  
                varName='valuePerQ',
                diffType='Gross',
                diffValue=0,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity12 = Sensitivity(
                globalVarBool=False,
                altID=0,
                bcnID=1,  
                # Invalid BCN object 
                bcnObj=self.alternative,  
                varName='valuePerQ',
                diffType='Percent',
                diffValue=0,
            )
        logger.info("Success!: %s", "Sensitivity-bcnObj tests passed.")

        return


    def test_missing_var(self):
        """
        Checks the Sensitivity Serializer throws a validation error when 
        variable to be changed passed in is invalid or of incorrect data type.
        """
        validVarNames = [
            'bcnID',
            'altID',
            'bcnType',
            'bcnSubType',
            'bcnName',
            'initialOcc',
            'bcnRealBool',
            'bcnInvestBool',
            'bcnLife',
            'rvBool',
            'rvOnly',
            'recurBool',
            'recurInterval',
            'recurVarRate',
            'recurVarValue',
            'recurEndDate',
            'valuePerQ',
            'quant',
            'quantVarRate',
            'quantVarValue',
            'quantUnit'
        ]
        # valid variables tests
        self.sensitivity13 = Sensitivity(
            globalVarBool=False,
            altID=0,
            bcnID=0,  
            bcnObj=self.bcn0, 
            varName='initialOcc',
            diffType='Gross',
            diffValue=1,
        )
        self.sensitivity14 = Sensitivity(
            globalVarBool=False,
            altID=0,
            bcnID=0,  
            bcnObj=self.bcn0, 
            varName='bcnLife',
            diffType='Gross',
            diffValue=2,
        )
        self.sensitivity15 = Sensitivity(
            globalVarBool=True,
            altID=0,
            bcnID=1,  
            bcnObj=self.bcn1, 
            varName='recurInterval',
            diffType='Gross',
            diffValue=1,
        )
        self.sensitivity16 = Sensitivity(
            globalVarBool=False,
            altID=0,
            bcnID=1,  
            bcnObj=self.bcn1, 
            varName='recurEndDate',
            diffType='Gross',
            diffValue=5,
        )
        self.sensitivity17 = Sensitivity(
            globalVarBool=False,
            altID=0,
            bcnID=1,  
            bcnObj=self.bcn1, 
            varName='quant',
            diffType='Percent',
            diffValue=20.0,
        )
        logger.info("Success!: %s", "Sensitivity-valid var tests passed.")

        # invalid variables tests
        with self.assertRaises(ValidationError):
            self.sensitivity18 = Sensitivity(
                globalVarBool=True,
                altID=0,
                bcnID=1,  
                bcnObj=self.bcn1,
                # Variable to change not supplied
                varName=None, 
                diffType='Percent',
                diffValue=0,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity19 = Sensitivity(
                globalVarBool=False,
                altID=0,
                bcnID=0,  
                bcnObj=self.bcn0,
                # Invalid type of variable to change
                varName=0, 
                diffType='Percent',
                diffValue=10.0,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity20 = Sensitivity(
                globalVarBool=False,
                altID=0,
                bcnID=0,  
                bcnObj=self.bcn0,
                # Invalid variable: not in BCN
                varName='serviceDate', 
                diffType='Gross',
                diffValue=0.0,
            )
        logger.info("Success!: %s", "Sensitivity-invalid var tests passed.")

        return


    def test_invalid_type(self):
        """
        Checks the Sensitivity Serializer throws a validation error when 
        difference type is invalid or of incorrect data type.
        """
        # valid diffType tests
        self.sensitivity21 = Sensitivity(
            globalVarBool=True,
            altID=0,
            bcnID=0,  
            bcnObj=self.bcn0, 
            varName='quant',
            diffType='Percent',
            diffValue=15.0,
        )
        self.sensitivity22 = Sensitivity(
            globalVarBool=False,
            altID=0,
            bcnID=1,  
            bcnObj=self.bcn1, 
            varName='valuePerQ',
            diffType='Gross',
            diffValue=1,
        )
        logger.info("Success!: %s", "Sensitivity-valid diffType tests passed.")

        # invalid diffType tests
        with self.assertRaises(ValidationError):
            self.sensitivity23 = Sensitivity(
                globalVarBool=False,
                altID=0,
                bcnID=0,  
                bcnObj=self.bcn0,
                varName='valuePerQ', 
                # Null diffType 
                diffType=None,  
                diffValue=0.0,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity24 = Sensitivity(
                globalVarBool=False,
                altID=0,
                bcnID=0,  
                bcnObj=self.bcn0,
                varName='valuePerQ', 
                # Invalid data type for diffType 
                diffType=1,  
                diffValue=0.0,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity25 = Sensitivity(
                globalVarBool=True,
                altID=0,
                bcnID=0,  
                bcnObj=self.bcn0,
                varName='valuePerQ',
                # Invalid diffType value 
                diffType='Change',  
                diffValue=0.0,
            )
        logger.info("Success!: %s", "Sensitivity-invalid diffType tests passed.")
        
        return


    def test_invalid_diff_val(self):
        """
        Checks the Sensitivity Serializer throws a validation error when 
        difference type, diffType, is invalid or of incorrect data type.
        """
        # invalid diffValue tests
        with self.assertRaises(ValidationError):
            self.sensitivity26 = Sensitivity(
                globalVarBool=True,
                altID=0,
                bcnID=0,  
                bcnObj=self.bcn0,
                varName='valuePerQ',
                diffType='Gross',  
                # Null diffValue value 
                diffValue=None,
            )
        with self.assertRaises(ValidationError):
            self.sensitivity27 = Sensitivity(
                globalVarBool=True,
                altID=0,
                bcnID=0,  
                bcnObj=self.bcn0,
                varName='valuePerQ',
                diffType='Gross',  
                # Invalid type (string) for diffValue 
                diffValue='1.0',
            )
        with self.assertRaises(ValidationError):
            self.sensitivity28 = Sensitivity(
                globalVarBool=True,
                altID=0,
                bcnID=0,  
                bcnObj=self.bcn0,
                varName='valuePerQ',
                diffType='Percent',  
                # Invalid type (string) for diffValue 
                diffValue='increase',
            )
        with self.assertRaises(ValidationError):
            self.sensitivity28 = Sensitivity(
                globalVarBool=True,
                altID=0,
                bcnID=0,  
                bcnObj=self.bcn0,
                varName='valuePerQ',
                diffType='Percent',  
                # Invalid type (infinite decimal) for diffValue 
                diffValue=float('inf'),
            )

        # valid diffValue tests
        self.sensitivity29 = Sensitivity(
            globalVarBool=True,
            altID=0,
            bcnID=0,  
            bcnObj=self.bcn0,
            varName='valuePerQ',
            diffType='Percent',  
            # Invalid type for diffValue 
            diffValue=-20.0,
        )
        self.sensitivity30 = Sensitivity(
            globalVarBool=True,
            altID=0,
            bcnID=0,  
            bcnObj=self.bcn0,
            varName='valuePerQ',
            diffType='Percent',  
            # Invalid type for diffValue 
            diffValue=0,
        )

        logger.info("Success!: %s", "Sensitivity-invalid diffVal tests passed.")
        
        return


    def test_generate_sensitivity_summary(self):
        #TODO: revisit later
        """
        Checks the Sensitivity Serializer throws a validation error when 
        difference type, diffType, is invalid or of incorrect data type.
        """
        #self.summary = 
        logger.info("Success!: %s", "Sensitivity-sensitivity generation tests passed.")
        
        return 
