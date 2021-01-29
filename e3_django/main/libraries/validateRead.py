from types import SimpleNamespace
import .discounting as discounting
import .flows as flows
from ../models import analysis, alternative, bcn, sensitivity, scenario


def validateFile(inputJSONFile):
    #! We require ELDST's help to set up, may be housed in another library.
    return 


def readFile(inputJSONFile):
    """
    Purpose: if file is properly validated, parse json into separate data list 
    for each user defined object type.
    """
    # Verify consistency of discounting input
    if discounting.checkDiscounting(): # ? Call to checkDiscounting()? where is this function defined
        pass

    else:
        # Call to Discounting Library to fill in missing information
        # Add missing information to appropriate place in list for the object(s) in question
    
    # If all required information is provided:
        # ! objectList = [[analysis], [projectType], [ObjectsToReport], ...]
    # elif some object(s) miss required elements / contain invalid entries: #! Required elements list?
        raise Exception('Invalid object provided to app)

    return objectList


def generateUserObjects(objectList):
    # Using objectList from readFile()
    for x in objectList:
        """
        Generate User-defined objects that call to Class constructors, and validate as constructed
        (validation is currently a separate method in each User Class:
            Analysis Class
            Alternative Class
            BCN Class
            Scenario Class
            Sensitivity Class)
        """
    
    return