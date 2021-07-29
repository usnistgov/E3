## imports everything. Imports are in order of their earliest call in main (not including debug mode calls
import validateRead
import json
import libraries.cashFlows
import models.userDefined.bcn
import models.userDefined.analysis
import models.bcnStorage
import models.userDefined.alternative
import models.totalRequiredFlows
import models.totalOptionalFlows
import libraries.measures
import models.alternativeSummary
import models.libraries.cashFlow

## Main-runs everything. Annotate any added code and keep new variable names clear or explicitly defined annotations
def E3main():
    debugMode = 1 ## Toggles debug mode. If "on" intermediate output in the main file will be printed to a log file for review. File is not currently formatted to keep debug code compact.
    ##userInput = request.json

    ## Parse JSON string. parsedInput will be a list of dictionaries with keynames corresponding to variable names in the JSON file
    ## Luke- with the new entry point feel free to move the parser wherever makes sense
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
    
    ## Luke - End input collection and formatting
    ## Calls constructors. This should generate all user defined objects through the call to generateUserObjects
    validateRead.generateUserObjects(analysisList,alternativeList,bcnList,sensitivityList,scenarioList)

    ## Loop through all bcn instances and generate all associated bcnStorage objects. The loop structure should work within django, if not we may need to move to a registry metaclass.
    ## The first call generates the cash and quantity flows for the bcn, the second generates the bcnStorage object for the associated bcn. Considering this process is repeated for the sensitivity
    ## and uncertainty calculations the following steps will eventually be moved to a separate function or possibly their own script if they take up a significant portion of the code; calculating and generating bcnStorage objects,
    ## calculating and generating total flows, calculating and generating measures, converting output to json format for passing user data back
    if analysis.outputRealBool == True: ##David - Added conditional to pull the right discount rate for the analysis
        discountRate = analysis.dRateReal
    else:
        discountRate = analysis.dRateNom
    studyPeriod = analysis.studyPeriod
    timestepComp = analysis.timestepComp ##David - Removed timestepCount = analysis.timestepCount and added timestepComp = analysis.timestepComp
    irrBoolean = analysis.irrBoolean. ##David - Removed hanging baselineBool variable and replaced it with irrBoolean
    reinvestRate = discountRate ##David - Added to initialize before call, separate in case we want to add reinvestRate as separate input at somepoint
    for bcn in bcn.objects.all():
        bcnNonDiscFlow, bcnDiscFlow, quantList = cashFlows.bcnFlow(discountRate,bcn,studyPeriod,timestepComp)
        bcnStorage(bcn.ID,bcn.bcnName,bcn.altID,bcn.type,bcn.subtype,bcn.tag,bcnNonDiscFlow,bcnDiscFlow,bcn.quantList,bcn.quantUnit)

    ## Generate the total flows for each alternative. First the list of all altIDs is generated. This is done by loopting through the alternative registry (or a metaclass can be used). The code then loops through the bcnStorage registry
    ## to sum all items related to a particular alternative. From there the code generates the totalRequiredFlows and totalOptionalFlows objects for each alternative via the call to cashFlows. altIDList will be used often.
    altIDList = []
    for alt in alternative.objects.all():
        altIDList.append(alt.altID)
        if alt.baselineBoolean == True:
            baselineID = alt.altID
            break ##David - Added break to preven unnecessray looping
        cashFlows.totalFlows(altID,studyPeriod,timestepComp,alt.baselineBoolean,bcnStorage.objects.all())        
    
    ## Create baseline measures
    for totRFlow in totalRequiredFlows.objects.all(): ##David - Changed how baseline Alternative is found to be a bit more explicit
        if totRFlow.baselineBool == True:
            baselineID = totRFlow.altID
            baselineAlt = totRFlow
            break
    baselineFlowList, baselineMeasList = measures.calcBaselineMeas(baselineAlt,irrBoolean)

    ## Create baseline tag measures
    baslineTagList = []
    for totOptFlow in totalOptionalFlows.objects.all(): ##David - Added "baselineTagList =" to call to calcBaselineTagMeas
        altID = totOptFlow.altID ##David - Added to prevent additional object attribute lookups
        if altID == baselineID: ##David - Added conditional to check that we are pulling the alternative for the baseline
            baselineTagList = measures.calcBaslineTagMeas(baselineTagList,baselineAlt,altID,totOptFlow.tag,totOptFlow.totalTagFlowDisc,totOptFlow.totTagQ,totOptFlow.quantUnits)

    ## Create baseline quantitiy attributes
    baselineQSum, baselineQUnits = quantList(baselineTagList)
    
    ## Construct Baseline alternative Summary Object
    baselineSummary = alternativeSummary(*baselineMeasList,baselineQSum,baselineQUnits,analysis.marr,None,None,None,None) ##David - initiated variable to store baselineSUmmary, may be useful in sensitivity or uncertainty

    ## Calculate alternative measures
    for totRFlow in totalRequiredFlows.objects.all():
        if totRFlow != baselineID:
            altID = totRFlow.altID
            altMeasList = calcAltMeas(altID,irrBoolean,baselineFlowList,reinvestRate,studyPeriod,totRFlow) ##David - Added irrBoolean and studyPeriod as input
            altTagMeasList = calcAltTagMeas(totalOptionalFlows.objects.all(),altMeasList,baselineTagList) ##David - Removed unneccesary inputs from call        
                     
            altQSum, altQUnits = quantList(altTagList)

            alternativeSummary(*altMeasList,altQSum,altQUnits,analysis.marr,*altTagMeasList)
            

    ## Write output (eventually move to separate library).
    ## Luke - At this point the altSummary objects should be converted to a JSON string and aggregated into a single json string to return to the user
    ## PSEUDOCODE (Feel free to move to a separate library if it makes more sense)
    ## reportType = analysis.objToReport
    ## if reportType == "FlowSummary":
    ##     convert totalRequiredFlows objects to JSON and add to output
    ## if reportType == "MeasureSummary":  ## Note that the "IRRSummary" type in analysis comes into play when calculating measures.
    ##     convert alternativeSummary objects to JSON and add to output
    ## The following are not needed now.
    ## if reportType == "SensitivitySummary":
    ##     convert sensitivitySummary objects to JSON and add to output
    ## if reportType == "UncertaintySummary":
    ##     convert uncertaintySummary objects to JSON and add to output

    ## Send output JSON to client
            
if __name == '__E3main__':
    app.run(debug=True)






            
