import .validateAndRead as vr
import .cashFlows as cf 
from ../models import bcn

# does this need to be wrapped in a Main class

def bcnLevelFlows(userObjects):
    # generate bcn level flows
    for obj in userObjects:
        if not isinstance(obj, bcn.bcnObject): continue
        bcnObject = obj

        bcnNonDiscFlow, bcnDiscFlow, quantList = cf.bcnFlow(
            bcnObject, studyPeriod, timestepCount
        )
        bcnStorage(
            bcnObject.bcnName, bcnObject.altID, bcnObject.bcnType, 
            bcnObject.bcnSubType, bcnObject.bcnTag,
            bcnNonDiscFlow, bcnDiscFlow, quantList,
            bcnObject.quantUnit
        )  # is this replacing the bcnObject

def main(inputFile):
    # validate and read
    vr.validateFile(inputFile)
    objectList = vr.readFile(inputFile)
    userObjects = vr.generateUserObjects(objectList)
    
    bcnLevelFlows(userObjects)

    # TODO rest