import /models/cashFlows
import /models/userDefined/bcn
import /models/userDefined/analysis
import /models/bcnStorage
import /models/userDefined/alternative
import /models/totalRequiredFlows
import /models/totalOptionalFlows
import /models/measures
import /models/alternativeSummary

def debugMode(userInput,parsedInput,analysisList,alternativeList,bcnList,sensitivityList,scenarioList,analysis):
    ## Open and add initial entries to log file
    mainDebugLog = open("Debug Log/main.txt","w")
    mainDebugLog.write("Basic Calculation Intermediate Output/n")
    mainDebugLog.write("-------------------------------------/n")
    mainDebugLog.write("User Input/n-------------------------------------/n" + userInput + "/n")
    mainDebugLog.write("JSON Dictionary/n-------------------------------------/n" + parsedInput + "/n")    
    mainDebugLog.write("Analysis List/n-------------------------------------/n" + analysisList + "/n")
    mainDebugLog.write("Alternative List/n-------------------------------------/n" + alternativeList + "/n")
    mainDebugLog.write("BCN List/n-------------------------------------/n" + bcnList + "/n")
    mainDebugLog.write("Sensitivity List/n-------------------------------------/n" + sensitivityList + "/n")
    mainDebugLog.write("Scenario List/n-------------------------------------/n" + scenarioList + "/n")
    mainDebugLog.write("ObjectList/n-------------------------------------/n")
    mainDebugLog.write("Analysis Objects/n-------------------------------------/n" + analysis.dir() + "/n")
    for alt in alternative._registry: mainDebugLog.write(alt.dir() + "/n")               ## Double check the inline syntax to make sure this works
    mainDebugLog.write("BCN Objects/n-------------------------------------/n")
    for bcn in bcn._registry: mainDebugLog.write(bcn.dir() + "/n")
    mainDebugLog.write("Alternative Objects/n-------------------------------------/n")
    for sens in sensitivity._registry: mainDebugLog.write(sens.dir() + "/n")
    mainDebugLog.write("Alternative Objects/n-------------------------------------/n")
    for unc in uncertainty._registry: mainDebugLog.write(unc.dir() + "/n")
    mainDebugLog.write("BCN Storage Objects/n-------------------------------------/n")
    for bcnStore in bcnStoraget._registry: mainDebugLog.write(bcnStore.dir() + "/n")
    mainDebugLog.write("Total Required Flows Objects/n-------------------------------------/n")
    for totRFlow in bcnStoraget._registry: mainDebugLog.write(totRFlow.dir() + "/n")
    mainDebugLog.write("Total Optional Flows Objects/n-------------------------------------/n")
    for TotOFlow in bcnStoraget._registry: mainDebugLog.write(totOFlow.dir() + "/n")

    ## Close log file
    debugLogMain.close()
