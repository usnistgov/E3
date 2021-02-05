from types import SimpleNamespace
import json
import .discounting as discounting
import .flows as flows
from .userDefined import (alternative, analysis, bcn, scenario, sensitivity)


def validateFile(dataFile):
    """
    This requires ELDST's help to set up, may be housed in another library. 
    ! For now, ignore.
    """
    return 


def readFile(inputJSONFile):
    """
    Purpose: if file is properly validated, parse json into separate data list 
    for each user defined object type.
    """
    if validateFile(inputJSONFile): 
        res = json.loads(inputJSONFile, object_hook=lambda d: SimpleNamespace(**d))
        analysisObj, alternativeObj, bcnObj, sensitivityObj, scenarioObj = res.analysisObject, res.alternativeObject, \
            res.bcnObject, res.sensitivityObject, scenarioObject

        objectList = [analysisObj, alternativeObj, bcnObj, sensitivityObj, scenarioObj] # List containing each User-Defined Object 

    # Verify consistency of discounting input
    if discounting.checkDiscounting(): # ? Call to checkDiscounting()? where is this function defined
        pass

    else:
        # Call to Discounting Library to fill in missing information
        # Add missing information to appropriate place in list for the object(s) in question
        pass
       
    # if some object(s) miss required elements / contain invalid entries: 
        raise Exception('Invalid entries provided, or objects missing required elements')

    return objectList # All required information are provided in objectList


def generateUserObjects(objectList):
    
    """
    Purpose: Call to Class constructors, with User-Defined Objects, and validates as constructed.
    Parameter: objectList (list): output object from readFile().

    Note: validation is currently a separate method in each User Class below:
        1. Analysis Class
        2. Alternative Class
        3. BCN Class
        4. Scenario Class
        5. Sensitivity Class)
    """
    Alternative(objectList[0])
    Analysis(objectList[1])
    BCN(objectList[2])
    Scenario(objectList[3])
    Sensitivity(objectList[4])

    return