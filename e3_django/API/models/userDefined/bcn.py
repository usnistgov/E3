from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import logging

logger = logging.getLogger(__name__)

class BCN(models.Model):

    def validateBCNObject(self, objectList):
        try:
            # Check here that initialOcc occurs at valid timestep

            # Based on chosen bcnType, check that all required inputs are included.
            if self.bcnType == 'Benefit':
                print("BCN is of 'Benefit' type.")
                # Check required fields for Benefit
                if not self.initialOcc or not self.bcnRealBool or not self.valuePerQ:
                    logger.error("Err: %s", "Invalid input(s) for BCN object using 'Benefit' type. \
                    Check that you have supplied all necessary fields: initialOcc, bcnRealBool, valuePerQ.")

                # Check optional fields for Benefit
                if not self.quantUnit:
                    logger.info("Note: %s", "Since quantUnit was not provided, value will be assumed to be in dollars.")
            
            elif self.bcnType == 'Cost':
                print("BCN is of 'Cost' type. Negative cost refers to Revenue.")
                # Check required fields for Cost
                if not self.bcnRealBool or not self.bcnInvestBool or not self.valuePerQ:
                    logger.error("Err %s", "Invalid input(s) for BCN object using 'Cost' type. \
                    Check that you have supplied all necessary fields: bcnRealBool, bcnInvestBool, valuePerQ.")

                # Check optional fields for Cost
                if not self.quantUnit:
                    logger.info("Note: %s", "Since quantUnit is not provided, value will be assumed to be in dollars.")    

            elif self.bcnType == 'NonMonetary':
                print("BCN is of 'NonMonetary' type.")
            # Check required fields for NonMonetary
                if not self.bcnTag or not self.quantUnit:
                    logger.error("Err %s", "Invalid input(s) for BCN object using 'NonMonetary' type. \
                    Check that you have supplied the field: 'bcnTag', 'quantUnit' required for non-monetary to simplify measure calculations.")

            else:
                logger.error("Err: BCN type is of unknown type")

            # Check conditional fields 
                if self.recurBool:
                    if not self.recurInterval or not self.recurVarRate or not self.recurVarValue:
                        logger.error("Err: %s", "Invalid input(s) for BCN object where 'recurBool' is True. \
                        Check that you have supplied all necessary fields: recurInterval, recurVarRate, recurVarValue.")
                if self.quantVarRate:
                    if not self.quantVarValue:
                        logger.error("Err: %s", "Invalid input(s) for BCN object where 'quantVarRate' exists. \
                        Check that you have supplied the field: quantVarValue.")

        except:
            logger.error("Err: %s", "Invalid input for BCN object. Check that they are correct data type and in range.")

        # Check optional fields 
        if not self.recurEndDate:
            logger.info("Note: %s", "Since recurEndDate is not provided, BCN will occur for the entire study period.")

        # (*) If blank, reports blank.
        if self.quantUnit == "":
            logger.warning('Warning: %s', 'The quantity unit supplied is blank.', extra=d)

        print("All inputs checked and verified. If no Err messages, BCN object can be created.")
        
        return