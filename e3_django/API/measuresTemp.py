## Move to measures library when time allows

import /models/cashFlows
import /models/userDefined/bcn
import /models/userDefined/analysis
import /models/bcnStorage
import /models/userDefined/alternative
import /models/totalRequiredFlows
import /models/totalOptionalFlows
import /models/measures
import /models/alternativeSummary

def calcBaselineMeas(): ## Still some redundancy in this file. Consider adding more granular functions
    ## FInd altID corresponding to baseline (make its own function?)
    for alt in alternative._registry:
        if alt.baselineBoolean == True:
            baselineID = alt.altID
            break 

    ## Get basline total Required FLows object 
    baselineTotFlows = [totRFlow for totRFlow in totalRequiredFlows._registry if totRFlow.altID == baselineID]

    ## Calculate baseline measures
    ## note that IRR still needs some work. If numpy.irr ends up being usable this code should be fine
    totalCostsBase = measures.sumCosts(baselineTotFlows.totCostsDisc)
    totalBenefitsBase = measures.sumBenefits(baselineTotFlows.totBenefitsDisc)
    totalInvBase = measures.sumInv(baselineTotFlows.totCostsInvDisc)
    totalNonInvBase = measures.sumNonInv(baselineTotFlows.totCostsNonInvDisc)
    if analysis.irrBoolean == true:
        irr = measures.measIRR(baselineTotFlows.totCostsDisc,baselineTotFlows.totBenefitsDisc)
    ## Generate List of Tags and store baseline output for each tag
    dpp = measures.dpp(totReqFlow.totCostDisc,totReqFlow.totBensDisc)
    spp = measures.spp(totReqFlow.totCostDisc,totReqFlow.totBensDisc)
    baselineTagList = []
    baselineTotalQuantList = []
    for totOptFlow in totalOptionalFlows._registry:
        ## Make own function
        if totOptFlow.altID == baselineID and totOptFlow.tag not in baselineTagList: ## Add new tags to baselineTagList
            baselineTagList.append([totOptFlow.tag,totOptFlow.totalTagFlowDisc,totOptFlow.totTagQ,totOptFlow.quantUnits])
        elif totOptFlow.altID == baselineID and totOptFlow.tag in baselineTagList:
            tagIndex = baselineTagList.index(totOptFlow.tag)  ## If tag exists, add the new values to the previous entries in baselineTagList. These are used for Total Quantity Flows outputs
            tagDiscFlow = [sum(x) for x in zip(totOptFlow.totalTagFlowDisc,baselineTagList[i][1])]
            tagQFlow = [sum(x) for x in zip(totOptFlow.totalTagFlowDisc,baselineTagList[i][2])]
            baselineTagList[i][1] = tagDiscFlow
            baselineTagList[i][1] = tagQFlow
            ## End make own function
            
    ## Make own function
    quantSum = []
    quantUnits = []
    for i in range(len(baselineTagList)):
        quantSum.append(baselineTagList[i][2])
        quantUnits.append(baselineTagList[0],baselineTagList[i][3])
    ## End make own function
        
    ##Create alternative summary object for baseline
    alternativeSummary(baselineID,totalBenefitsBase,totalCostsBase,totalInvBase,totalNonInvBase,none,none,none,irr,none,dpp,spp,none,
                       quantSum,quantUnits,analysis.marr,none,none,none,none)

    return baselineID, baselineTagList

def calcAltMeas(baselineID, baselineTagList):
    ## Use baselineID to find baseline altSummary Object

    ## define totalCostsBase, totalBenefitsBase, totalCostsInvBase, totalCostsNonInvBase using altSummary object for baseline
    
    ## Loop through remainder of total Required Flows objects and calculate their measures.
    for totReqFlow in totalRequiredFlows._registry:
        if totReqFlow.altID != baselineID:
            totalCosts = measures.sumCosts(totReqFlow.totCostsDisc)
            totalBenefitsBase = measures.sumBenefits(totReqFlow.totBenefitsDisc)
            totalInvBase = measures.sumInv(totReqFlow.totCostsInvDisc)
            totalNonInvBase = measures.sumNonInv(totReqFlow.totCostsNonInvDisc)
            if analysis.irrBoolean == true:
                irr = measures.measIRR(totReqFlow.totCostsDisc,totReqFlow.totBenefitsDisc)  ## Assuming simplest case, this may need adjustment if we can't rely on numpy.irr
            netBenefits = measures.netBenefits(totalBenefits,totalCosts,totalBenefitsBase,totalCostsBase)
            netSavings = measures.netSavings(totalCosts,totalCostsBase)
            bcr = measures.measBCR(netSavings,totalCostsInv,totalCostsInvBase)
            sir = measures.measSIR(totalCostsInv,totalCostsNonInv,totalCostInvBase,totalCostsNonInvBase)
            airr = measures.measAIRR(analysis.reinvestRate,sir)
            dpp = measures.dpp(totReqFlow.totCostDisc,totReqFlow.totBensDisc)
            spp = measures.spp(totReqFlow.totCostDisc,totReqFlow.totBensDisc)
    ## Loop through tags in the current alt to see if they match the baseline tags. If so calculate the tag related measures. If not we handle it in writing the output file
    altTagList = []
    quantMeasList = []
    deltaQuant = []
    nsDeltaQuant = []
    nsPercQuant = []
    nsElasticityQuant = []
    for totOptFlow in totalOptionalFlows._registry:
        if totOptFlow.altID == totOptFlow.altID:
            ## Make own function
            if totOptFlow.tag not in altTagList: ## Add new tags to baselineTagList
                altTagList.append([totOptFlow.tag,totOptFlow.totalTagFlowDisc,totOptFlow.totTagQ,totOptFlow.quantUnits])
            elif totOptFlow.tag in altTagList:
                tagIndex = altTagList.index(totOptFlow.tag)  ## If tag exists, add the new values to the previous entries in baselineTagList. These are used for Total Quantity Flows outputs
                tagDiscFlow = [sum(x) for x in zip(totOptFlow.totalTagFlowDisc,altTagList[i][1])]
                tagQFlow = [sum(x) for x in zip(totOptFlow.totalTagFlowDisc,altTagList[i][2])]
                altTagList[i][1] = tagDiscFlow
                altTagList[i][1] = tagQFlow
            ## End make own function
    for baslineTag in baselineTagList:
        for altTag in altTagList:
            if altTag[0] == baselineTag[0]:
                deltaQuant.append(altTag[0],measures.measDeltaQ(baselineTag[2],altTag[2]))
                nsPerQuant.append(altTag[0],measures.measNSPerQ(netSavings,baselineTag[2]))
                nsPerPctQuant.append(altTag[0],measures.measNSPerPctQ(netSavings,deltaQ,baselineTag[2]))
                nsElasticityQuant.append(altTag[0],measures.measNSElasticity(netSavings,totalCosts,deltaQ,baselineTag[2]))
                    
    ## Make own function
    quantSum = []
    quantUnits = []
    for i in range(len(altTagList)):
        quantSum.append(altTagList[i][2])
        quantUnits.append([altTagList[0],altTagList[i][3]])
    ## End make own function

    ##Create alternative summary object for baseline
    alternativeSummary(baselineID,totalBenefits,totalCosts,totalInv,totalNonInv,netBenefits,netSavings,sir,irr,airr,dpp,spp,bcr,
                       quantSum,quantUnits,analysis.marr,deltaQuant,nsDeltaQuant,nsPercQuant,nsELasticityQuant)







                    
