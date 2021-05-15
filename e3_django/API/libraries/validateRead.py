import json
from API.libraries import discounting
from API.libraries import cashFlow 
from API.models.userDefined import alternative, analysis, bcn, scenario, sensitivity
from types import SimpleNamespace

def validateFile(dataFile):
    """
    This requires ELDST's help to set up, may be housed in another library. 
    Output: Boolean, indicating if file is valid.
    ! For now, ignore this
    """
    print("File was successfully validated.")
    return True

def readFile(inputJSONFile):
    """
    Purpose: if file is properly validated, parse json into separate data list 
    for each user defined object type.
    """
    if validateFile(inputJSONFile): # file is valid
        res = json.loads(inputJSONFile, object_hook=lambda d: SimpleNamespace(**d))
        analysisObj, alternativeObj, bcnObj, sensitivityObj, scenarioObj = \
            res.analysisObject, res.alternativeObject, res.bcnObject, res.sensitivityObject, scenarioObject # load into user-defined objects

        objectList = [analysisObj, alternativeObj, bcnObj, sensitivityObj, scenarioObj] # List containing each user-defined object
    else:
        raise Exception('File is not valid')

    # Verify consistency of discounting input
    if discounting.checkDiscounting(): # ? Call to checkDiscounting()? where is this function defined
        pass

    else:
        # Call to Discounting Library to fill in missing information
        # Add missing information to appropriate place in list for the object(s) in question
        # ?: This part is checked upon Object creation - is discounting.checkDiscounting necessary in this case?
        pass

    if all(objectList) and (analysisObj.analysisType and analysisObj.projectType and analysisObj.objToReport, analysisObj.studyPeriod,\
        analysisObj.baseDate, analysisObj.serviceDate, analysisObj.timestepVal, analysisObj.timestepComp, analysisObj.outputRealBool,\
        analysisObj.interestRate, analysisObj.dRateReal, analysisObj.dRateNom, analysisObj.inflationRate, analysisObj.Marr, \
        analysisObj.reinvestRate, analysisObj.incomeRateFed, analysisObj.incomeRateOther, analysisObj.noAlt, analysisObj.location) \
        and (alternativeObj.altID, alternativeObj.altName, alternativeObj.altBCNList, alternativeObj.baselineBool):

        return objectList 

    else: 
        #some object(s) miss required elements / contain invalid entries: 
        raise Exception('Invalid entries provided, or objects missing required elements')

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

