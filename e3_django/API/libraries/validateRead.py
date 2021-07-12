import json
from . import discounting as discounting
from API.models.userDefined import analysis
from ..models import alternativeSummary
#from ..models.userDefined import alternative, bcn, scenario, sensitivity

from types import SimpleNamespace
import logging

logger = logging.getLogger(__name__)

def validateFile(dataFile):
    """
    This requires ELDST's help to set up, may be housed in another library. 
    Output: Boolean, indicating if file is valid. For now, ignore this.
    """
    return True


def readFile(inputJSONFile):
    """
    Purpose: if file is properly validated, parse json into separate data list 
    for each user defined object type.
    """
    if validateFile(inputJSONFile): # Check that file is valid
        res = json.loads(inputJSONFile, object_hook=lambda d: SimpleNamespace(**d))
        analysisObj, alternativeObj, bcnObj, scenarioObj, sensitivityObj  = \
            res.analysisObject, res.alternativeObject, res.bcnObject, res.scenarioObject, res.sensitivityObject # load into user-defined objects

        objectList = [analysisObj, alternativeObj, bcnObj, scenarioObj, sensitivityObj] # List containing each user-defined object
    else:
        raise Exception('Err: File is not valid')

    # Verify consistency of discounting input
    if analysis.validateDiscountRate() == True:
        # If discounting input is valid: pass.
        pass

    else: # discounting input is NOT valid:
        # Call to Discounting Library to fill in missing information
        # I.e., add missing information to appropriate place in list for the object(s) in question
        if not analysisObj.inflationRate:
            analysisObj.inflationRate = discounting.inflationRateCalc(analysisObj.dRateNorm, analysisObj.dRateReal)
        
        elif analysisObj.dRateNorm:
            analysisObj.dRateNorm = discounting.dRateNomCalc(analysisObj.inflationRate, analysisObj.dRateReal)
        
        elif analysisObj.dRateReal:
            analysisObj.dRateReal = discounting.dRateRealCalc(analysisObj.dRateNorm, analysisObj.inflationRate)
        else:
            raise Exception("Err: Invalid discount rate")

    return generateUserObjects(objectList) 

def generateUserObjects(objectList):
    """
    Purpose: Call to Class constructors with User-Defined Objects, and validates as constructed.
    Parameter: objectList (array): output object from readFile().
    Output: list of user-defined objects if all inputs are proper, else raises Exception

    Note: validation is currently a separate method in each User Class below:
        1. Analysis Class
        2. Alternative Class
        3. BCN Class
        4. Scenario Class
        5. Sensitivity Class)
    """
    try: analysisObj = analysis.Analysis(objectList[0])
    except: logger.error('Error: %s', 'Invalid entries provided or missing required elements in Analysis Object.')
    
    try: alternativeObj = analysis.Alternative(objectList[1])
    except: logger.warning('Warning: %s', 'Invalid entries provided or missing required elements in Alternative Object.')
   
    try: bcnObj = analysis.BCN(objectList[2])
    except: logger.warning('Warning: %s', 'Invalid entries provided or missing required elements in BCN Object.')
    
    try: scenarioObj = analysis.Scenario(objectList[3])
    except: logger.warning('Warning: %s', 'Invalid entries provided or missing required elements in Scenario Object.')

    try: sensitivityObj = analysis.Sensitivity(objectList[4])
    except: logger.warning('Warning: %s', 'Invalid entries provided or missing required elements in Sensitivity Object.')
    

    if analysisObj and alternativeObj and bcnObj and scenarioObj and sensitivityObj:
        return analysisObj, alternativeObj, bcnObj, scenarioObj, sensitivityObj
    else:
        logger.warning('Warning: %s', 'Some objects were not generated. Please check messages to update inputs.')

