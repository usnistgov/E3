## imports everything. Imports are in order of their earliest call in main (not including debug mode calls
import validateRead
import json
import /models/cashFlows
import /models/userDefined/bcn
import /models/userDefined/analysis
import /models/bcnStorage
import /models/userDefined/alternative
import /models/totalRequiredFlows
import /models/totalOptionalFlows
import /models/measures
import /models/alternativeSummary
from flask import request, response

## Create app and set it to listen for incoming POST requests
app = FLASK(__E3main__)
@app.route('/', methods=['GET','POST']) ## We'll need to set the app route at some point
## Main-runs everything. Annotate any added code and keep new variable names clear or explicitly defined annotations
def E3main():
    debugMode = 1 ## Toggles debug mode. If "on" intermediate output in the main file will be printed to a log file for review. File is not currently formatted to keep debug code compact.
    userInput = request.json
    
    ## Parse JSON string. parsedInput will be a list of dictionaries with keynames corresponding to variable names in the JSON file
    parsedInput = json.loads(userInput)

    ## Generate input strings for user defined object construction. parsedInput.items will return a list of the tuples then the for loop generates the list in a form usable for input. For inputs with multiple objects
    ## a subList is generated for each object is generated and then appended to the full list. For now I have this in main and done using repeated calls, this will be streamlined. I'll eventually make the "for" loops their own function to keep main clean and avoid difficulties debugging
    dictToListTemp = parsedInput[analysisObject].items()
    analysisList = []
    for item in dictToListTemp:
        analysisList.append(item[1])

    dictToListTemp = parsedInput[alternativeObjects].items()
    alternativeList = []
    for item in dictToListTemp:
        subList = []
        for subItem in item:
            subList.append(subItem[1])
        alternativeList.append(sublist)

    dictToListTemp = parsedInput[bcnObjects].items()
    bcnList = []
    for item in dictToListTemp:
        subList = []
        for subItem in item:
            subList.append(subItem[1])
        bcnList.append(sublist)

    dictToListTemp = parsedInput[sensitivityObjects].items()
    sensitivityList = []
    for item in dictToListTemp:
        subList = []
        for subItem in item:
            subList.append(subItem[1])
        sensitivityList.append(sublist)

    dictToListTemp = parsedInput[scenarioObjects].items()
    scenarioList = []
    for item in dictToListTemp:
        subList = []
        for subItem in item:
            subList.append(subItem[1])
        scenarioList.append(sublist)

    ## Calls constructors. This should generate all user defined objects through the call to generateUserObjects
    validateRead.generateUserObjects(analysisList,alternativeList,bcnList,sensitivityList,scenarioList)

    ## Loop through all bcn instances and generate all associated bcnStorage objects. May need to add _registry = [] in the class definitionsto make the class iterable or make a metaclass. Either works but the following
    ## assumes a registry is used. The first call generates the cash and quantity flows for the bcn, the second generates the bcnStorage object for the associated bcn. Considering this process is repeated for the sensitivity
    ## and uncertainty calculations the following steps will eventually be moved to a separate function or possibly their own script if they take up a significant portion of the code; calculating and generating bcnStorage objects,
    ## calculating and generating total flows, calculating and generating measures, converting output to json format for passing user data back
    for bcn in bcn._registry:
        bcnNonDiscFlow, bcnDiscFlow, quantList = cashFlows.bcnFlow(analysis.discountRate,bcn,analysis.studyPeriod,analysis.timestepCount)
        bcnStorage(bcn.ID,bcn.bcnName,bcn.altID,bcn.type,bcn.subtype,bcn.tag,bcnNonDiscFlow,bcnDiscFlow,bcn.quantList,bcn.quantUnit)

    ## Generate the total flows for each alternative. First the list of all altIDs is generated. This is done by loopting through the alternative registry (or a metaclass can be used). The code then loops through the bcnStorage registry
    ## to sum all items related to a particular alternative. From there the code generates the totalRequiredFlows and totalOptionalFlows objects for each alternative via the call to cashFlows. altIDList will be used often.
    altIDList = []
    for alt in alternative._registry:
        altIDList.append(alt.altID)

    for altID in altIDList:
        cashFlows.(bcnStorage._registry,altID)
    
    ## Calculate measures for baseline and construct it's alternative summary object.
    baselineID, baselineTagList = measures.calcBaselineMeas()

    ## calculate measures for other alts and construct their alternative summary objects.
    measures.calcAltMeas(baselineID, baselineTagList)

    ## Write output (eventually move to separate library).
    basicOutputString = "'basicOutput':\n[{\n'alternativeSummary':\n

    for altSum in alternativeSummary._registry:
        basicOutputString = basicOutputString + "{" json.dumps(altSum.__dict__) + ","
    
    basicOutputString = basicOutputString[:-1] + "}\n}]"

    ## Send data to client
    return basicOutputString
            
if __name == '__E3main__':
    app.run(debug=True)






            
