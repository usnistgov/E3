from django.db import models
import numpy as np


def checkCosts(totCostDisc,totCostDiscInv,totCostDiscNonInv,totFlowDisc,totBenefitsDisc):
	## Should be run after sumCosts through sumBenefits
	if totCostDisc != totCostDiscInv + totCostDiscNonInv or totFlowDisc != totCostDiscInv + totCostDiscNonInv - totBenefitsDisc:
		raise Exception("There was an error in calculation")

	return

def sumCosts(totCostDisc):
	return np.sum(totCostDisc)

def sumBenefits(totBenefitsDisc):
	return np.sum(totBenefitsDisc)

def sumInv(totCostsInvDisc):
	return np.sum(totCostsInvDisc)

def sumNonInv(totCostsNonInvDisc):
	return np.sum(totCostsNonInvDisc)


def netBenefits(totalBenefits, totalCosts, totalBenefitsBase, totalCostsBase):
	netBenefits = 0
	netBenefits = (totalBenefits[])

	return netBenefits

def netSavings(totalCosts, totalCostsBase):
	netSavings = 0
	return netSavings

def measBCR(netSavings, totalCostsInv, totalCostsInvBase):
	return 

def measSIR(totalCostsInv, totalCostsNonInv, totalCostsInvBase, totalCostsNonInvBase):
	return 

def measAIRR(sir):
	return 

def measDeltaQ(altID, altIDBase, tag):
	return

def measNSPerQ(netSavings, altID, altIDBase, tag):
	return

def measNSPerPctQ(netSavings, altID, altIDBase, tag):
	return

def measNSPerPctQ(netSavings, altID, altIDBase, tag):
	measNSPerPctQ = 0
	return measNSPerPctQ

def measNSElasticity(altID, altIDBase, tag):
	measNSElasticity = 0
	return measNSElasticity

def measIRR(self, altID):
    	""" Note from pseudocode docs: Technically speaking should be solving this, but the solution requires a 
		root finding algorithm and repeatedly updating cash flows to obtain.
		"""
	measIRR = numpy.irr(totBenefitsNonDisc(), totCostsNonDisc)
	return measIRR

def measDPP(self, altID):
	return

def totalQuant(self, altID, tag):
	quantSum = 0
	#if tag == totalOptionalCashFlow.tag:
    		
	return quantSum, quantUnitstotalOptionalFlows

##Moved to quantList function
##def totalQuant(self, altID, tag):
##        quantSum = 0
##    		
##	return quantSum, quantUnits

def calcBaselineMeas(baselineTotFlows): ## Still a lot of redundancy in here. Consider adding more granular functions. Same as for the following function
    totFlows = np.subtract(baselineTotFlows.totCostDisc,baselineTotFlows.totBenefitsDisc)
    totFlowsNonDisc = np.subtract(baselineTotFlows.totCostNonDisc,baselineTotFlows.totBenefitsNonDisc)
    totCosts = baselineTotFlows.totCostDisc
    totBens = baselineTotFlows.totBenefitsDisc
    totCostsInv = baselineTotFlows.totCostsInvDisc
    totCostsNonInv = baselineTotFlows.totCostsNonInvDisc
    baselineFlowList = [totFlows,totCosts,totBens,totCostsInv,totCostsNonInv]

    totalCostsBase = measures.sumCosts(totCosts)
    totalBenefitsBase = measures.sumBenefits(totBens)
    totalInvBase = measures.sumInv(totCostsInv)
    totalNonInvBase = measures.sumNonInv(totCostsNonInv)
    if analysis.irrBoolean == True:
        irr = measures.measIRR(totFlowsNonDisc)
    else:
        irr = None
    dpp = measures.measPaybackPeriod(totCosts,totBens) 
    spp = measures.measPaybackPeriod(totReqFlow.totCostNonDisc,totReqFlow.totBensNonDisc) ## Only call to these two attributes

    baselineMeasList = [baselineID, totalBenefitsBase, totalCostsBase, totalInvBase, totalNonInvBase, None, None, irr,
                        None, dpp, spp, None]

                       quantSum,quantUnits,analysis.marr,deltaQuant,nsDeltaQuant,nsPercQuant,nsELasticityQuant

    return baselineFlowList, baselineMeasList

def calcBaslineTagMeas(baselineTagList,baselineAlt,altID,tag,flowDisc,totTagQ)
    if altID == baselineID and tag not in baselineTagList: ## Add new tags to baselineTagList
        baselineTagList.append(tag,flowDIsc,totTagQ,units])
    elif altID == baselineID and tag in baselineTagList:
        tagIndex = baselineTagList.index(tag)  ## If tag exists, add the new values to the previous entries in baselineTagList. These are used for Total Quantity Flows outputs
        baselineTagList[i][1] = np.add(flowDisc,baselineTagList[i][1])
        baselineTagList[i][2] = np.add(totTagQ,baselineTagList[i][2])

    return
            
def quantList(baselineTagList)
    quantSum = []
    quantUnits = []
    for i in range(len(baselineTagList)):
        quantSum.append(baselineTagList[i][2])
        quantUnits.append(baselineTagList[0],baselineTagList[i][3])

    return quantSum, quantUnits

def calcAltMeas(altID, baselineFlowList,reinvestRate,totRFlow):
## Loop through remainder of total Required Flows objects and calculate their measures.
        totFlows = np.subtract(totReqFlow.totCostDisc,totReqFlow.totBenefitsDisc)
        totFlowsNonDisc = np.subtract(altTotFlows.totCostNonDisc,altTotFlows.totBenefitsNonDisc)
        totCosts = totReqFlow.totCostDisc
        totBens = totReqFlow.totBenefitsDisc
        totCostsInv = totReqFlow.totCostsInvDisc
        totCostsNonInv = totReqFlow.totCostsNonInvDisc
    
        totalCosts = measures.sumCosts(totCosts)
        totalBenefitsBase = measures.sumBenefits(totBens)
        totalInvBase = measures.sumInv(totCostsInv)
        totalNonInvBase = measures.sumNonInv(totCostsNonInv)
        if analysis.irrBoolean == True:
             irr = measures.measIRR(totFlowsNonDisc)
        else:
             irr = None
        netBenefits = measures.netBenefits(totalBenefits,totalCosts,baselineFlowList[2],baselineFlowList[1])
        netSavings = measures.netSavings(totalCosts,baselineFlowList[1])
        bcr = measures.measBCR(netSavings,totalCostsInv,baselineFlowList[3])
        sir = measures.measSIR(totalCostsInv,totalCostsNonInv,baselineFlowList[3],baselineFlowList[4])
        airr = measures.measAIRR(reinvestRate,sir)
        dpp = measures.measPaybackPeriod(totCosts,totBens)
        spp = measures.measPaybackPeriod(totReqFlow.totCostNonDisc,totReqFlow.totBensNonDisc)

        altMeasList = [altID, totalBenefits, totalCosts, totalInv, totalNonInv, netSavings, sir, irr, airr,
                       dpp, spp, bcr]
            
        return altMeasList

def calcAltTagMeas(altMeasList,baselineTagList,tag,totalTagFlowDisc,totTagQ,quantUnits)
    if tag not in altTagList: ## Add new tags to baselineTagList
          altTagList.append([tag,totalTagFlowDisc,totTagQ,quantUnits])
    elif tag in altTagList:
        tagIndex = altTagList.index(tag)  ## If tag exists, add the new values to the previous entries in baselineTagList. These are used for Total Quantity Flows outputs
        altTagList[i][1] = np.add(totalTagFlowDisc,altTagList[i][1])
        altTagList[i][2] = np.add(totalTagFlowDisc,altTagList[i][2])

    for baslineTag in baselineTagList:
        for altTag in altTagList:
            if altTag[0] not in baselineTag:
                deltaQ = altTag[2]
                deltaQuant.append([altTag[0],deltaQ])
                nsPerQuant.append([altTag[0],measures.measNSPerQ(altMeasList[5],baselineTag[2])])
                nsPerPctQuant.append([altTag[0],"Infinite")
                nsElasticityQuant.append([altTag[0],"Infinite")
            elif altTag[0] == baselineTag[0]:
                deltaQ = measures.measDeltaQ(baselineTag[2],altTag[2])
                deltaQuant.append([altTag[0],deltaQ])
                nsPerQuant.append([altTag[0],measures.measNSPerQ(altMeasList[5],baselineTag[2])])
                nsPerPctQuant.append([altTag[0],measures.measNSPerPctQ(altMeasList[5],deltaQ,baselineTag[2])])
                nsElasticityQuant.append([altTag[0],measures.measNSElasticity(altMeasList[5],altMeasList[2],deltaQ,baselineTag[2])])
                
    return [deltaQuant,nsPerQuant,nsPerPctQuant,nsElasticityQuant]
