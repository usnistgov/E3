#from ..  import libraries.validateRead as vr

"""
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
        )  
"""

def main(inputFile):
    # Validate file and generate user-defined objects.
    validated_file = vr.validateFile(inputFile)
    validated_object_list = vr.readFile(validated_file)
    vr.generateUserObjects(validated_object_list)

    # Generate BCN level flows 
    
    # Generate Total Cash Flows using totalFlows from cashFlows library

    # Calculate measures 
    
    # Write to output file
    with open("../../sampleUserOutput_E3.json", mode='w') as f:
        f.write(OutputInJSON) 

    return