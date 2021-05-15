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

## Main-runs everything. Annotate any added code and keep new variable names clear or explicitly defined annotations
def main():
    debugMode = 1 ## Toggles debug mode. If "on" intermediate output in the main file will be printed to a log file for review. File is not currently formatted to keep debug code compact. I'll eventually be moving these calls to their own script
    ## Open and add initial entries to log file if debug mode is on
    if debugMode == 1:
        mainDebugLog = open("Debug Log/main.txt","w")
        mainDebugLog.write("Basic Calculation Intermediate Output/n")
        mainDebugLog.write("-------------------------------------/n")
        
    ## Script to get JSON string from user input. Script not written yet so output for now "userInput" needs to be defined manually for debugging purposes
    ## This script will also do some basic checks on input to verify there are no invalid characters. SOme validate and read calls will need to be made here
    userInput = " "
    mainDebugLog.write("User Input/n-------------------------------------/n" + userInput + "/n") if debugMode == 1
    
    ## Parse JSON string. parsedInput will be a list of dictionaries with keynames corresponding to variable names in the JSON file
    parsedInput = json.loads(userInput)
    mainDebugLog.write("JSON Dictionary/n-------------------------------------/n" + parsedInput + "/n") if debugMode == 1

    ## Generate input strings for user defined object construction. parsedInput.items will return a list of the tuples then the for loop generates the list in a form usable for input. For inputs with multiple objects
    ## a subList is generated for each object is generated and then appended to the full list. For now I have this in main. I'll eventually make the "for" loops their own function to keep main clean and avoid difficulties debugging
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

    ## Optional Log
    mainDebugLog.write("Analysis List/n-------------------------------------/n" + analysisList + "/n") if debugMode == 1
    mainDebugLog.write("Alternative List/n-------------------------------------/n" + alternativeList + "/n") if debugMode == 1
    mainDebugLog.write("BCN List/n-------------------------------------/n" + bcnList + "/n") if debugMode == 1
    mainDebugLog.write("Sensitivity List/n-------------------------------------/n" + sensitivityList + "/n") if debugMode == 1
    mainDebugLog.write("Scenario List/n-------------------------------------/n" + scenarioList + "/n") if debugMode == 1
    
    ## Calls constructors. This should generate all user defined objects through the call to generateUserObjects
    validateRead.generateUserObjects(analysisList,alternativeList,bcnList,sensitivityList,scenarioList)

   ## Optional Log 
    mainDebugLog.write("ObjectList/n-------------------------------------/n") if debugMode == 1
    mainDebugLog.write("Analysis Objects/n-------------------------------------/n" + analysis.dir() + "/n") if debugMode == 1
    mainDebugLog.write("Alternative Objects/n-------------------------------------/n") if debugMode == 1
    if debugMode == 1: for alt in alternative._registry: mainDebugLog.write(alt.dir() + "/n")               ## Double check the inline syntax to make sure this works
    mainDebugLog.write("BCN Objects/n-------------------------------------/n") if debugMode == 1
    if debugMode == 1: for bcn in bcn._registry: mainDebugLog.write(bcn.dir() + "/n")
    mainDebugLog.write("Alternative Objects/n-------------------------------------/n") if debugMode == 1
    if debugMode == 1: for sens in sensitivity._registry: mainDebugLog.write(sens.dir() + "/n")
    mainDebugLog.write("Alternative Objects/n-------------------------------------/n") if debugMode == 1
    if debugMode == 1: for unc in uncertainty._registry: mainDebugLog.write(unc.dir() + "/n")

    ## Loop through all bcn instances and generate all associated bcnStorage objects. May need to add _registry = [] in the class definitionsto make the class iterable or make a metaclass. Either works but the following
    ## assumes a registry is used. The first call generates the cash and quantity flows for the bcn, the second generates the bcnStorage object for the associated bcn. Considering this process is repeated for the sensitivity
    ## and uncertainty calculations the following steps will eventually be moved to a separate function or possibly their own script if they take up a significant portion of the code; calculating and generating bcnStorage objects,
    ## calculating and generating total flows, calculating and generating measures, converting output to json format for passing user data back
    for bcn in bcn._registry:
        bcnNonDiscFlow, bcnDiscFlow, quantList = cashFlows.bcnFlow(analysis.discountRate,bcn,analysis.studyPeriod,analysis.timestepCount)
        bcnStorage(bcn.ID,bcn.bcnName,bcn.altID,bcn.type,bcn.subtype,bcn.tag,bcnNonDiscFlow,bcnDiscFlow,bcn.quantList,bcn.quantUnit)

    ## Optional Log
    mainDebugLog.write("BCN Storage Objects/n-------------------------------------/n") if debugMode == 1
     if debugMode == 1: for bcnStore in bcnStoraget._registry: mainDebugLog.write(bcnStore.dir() + "/n")

    ## Generate the total flows for each alternative. First the list of all altIDs is generated. This is done by loopting through the alternative registry (or a metaclass can be used). The code then loops through the bcnStorage registry
    ## to sum all items related to a particular alternative. From there the code generates the totalRequiredFlows and totalOptionalFlows objects for each alternative via the call to cashFlows. altIDList will be used often.
    altIDList = []
    for alt in alternative._registry:
        altIDList.append(alt.altID)

    for altID in altIDList:
        cashFlows.(bcnStorage._registry,altID)

    ##c Optional Log  
    mainDebugLog.write("Total Required Flows Objects/n-------------------------------------/n") if debugMode == 1
    if debugMode == 1: for totRFlow in bcnStoraget._registry: mainDebugLog.write(totRFlow.dir() + "/n")
    mainDebugLog.write("Total Optional Flows Objects/n-------------------------------------/n") if debugMode == 1
    if debugMode == 1: for TotOFlow in bcnStoraget._registry: mainDebugLog.write(totOFlow.dir() + "/n")
    
    ## Calculate measures.
    ## FInd altID corresponding to baseline (make its own function?)
    for alt in alternative._registry:
        if alt.baselineBoolean == True:
            baselineID = alt.altID
            break
        
    ## Get basline total Required FLows object 
    baselineTotFlows = [totRFlow for totRFlow in totalRequiredFlows._registry if totRFlow.altID == baselineID]
    
    ## Calculate baseline measures (currently doens't contain "tag" based calculations as there are a few extra steps required and I'm trying to find the best place to add them
    ## note that IRR still needs some work
    totalCostsBase = measures.sumCosts(baselineTotFlows.totCostsDisc)
    totalBenefitsBase = measures.sumBenefits(baselineTotFlows.totBenefitsDisc)
    totalInvBase = measures.sumInv(baselineTotFlows.totCostsInvDisc)
    totalNonInvBase = measures.sumNonInv(baselineTotFlows.totCostsNonInvDisc)
    if analysis.irrBoolean == true:
        irr = measures.irr(baselineTotFlows.totCostsDisc,baselineTotFlows.totBenefitsDisc)
    
    ## Loop through remainder of total Required Flows objects and calculate their measures.
    for totReqFlow in totalRequiredFlows._registry:
        if totReqFlow.altID != baselineID:
            totalCosts = measures.sumCosts(totReqFlow.totCostsDisc)
            totalBenefitsBase = measures.sumBenefits(totReqFlow.totBenefitsDisc)
            totalInvBase = measures.sumInv(totReqFlow.totCostsInvDisc)
            totalNonInvBase = measures.sumNonInv(totReqFlow.totCostsNonInvDisc)
            if analysis.irrBoolean == true:
                irr = measures.irr(totReqFlow.totCostsDisc,totReqFlow.totBenefitsDisc)
            netBenefits = measures.netBenefits(totalBenefits,totalCosts,totalBenefitsBase,totalBenefitsCost)
            netSavings = measures.netSavings(totalCosts,totalCostsBase)
            bcr = measures.measBCR(netSavings,totalCostsInv,totalCostsInvBase)
            sir = measures.measSIR(totalCostsInv,totalCostsNonInv,totalCostInvBase,totalCostsNonInvBase)
            airr = measures.measAIRR(analysis.reinvestRate,sir)
            ##Add tag/optional flow calculations here
            ##Generate alternative summary object. Do onve tag calculations are complete

    ## Close log file
    debugLogMain.close()
