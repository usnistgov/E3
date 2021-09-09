import numpy as np

##-------------------------------##
def sumCosts(totCostDisc):
	return np.sum(totCostDisc)

##-------------------------------##
def sumBenefits(totBenefitsDisc):
	return np.sum(totBenefitsDisc)

##-------------------------------##
def sumInv(totCostsInvDisc):
	return np.sum(totCostsInvDisc)

##-------------------------------##
def sumNonInv(totCostsNonInvDisc):
	return np.sum(totCostsNonInvDisc)
    
##-------------------------------##
def netBenefits(totalBenefits, totalCosts, totalBenefitsBase, totalCostsBase):
	return (totalBenefits-totalBenefitsBase)-(totalCosts-totalCostsBase)

##-------------------------------##
def netSavings(totalCosts, totalCostsBase):
	return (totalCostsBase - totalCosts)

##-------------------------------##
def checkCosts(totCostDisc,totCostDiscInv,totCostDiscNonInv):
	## Should be run after sumCosts through sumBenefits
	if totCostDisc != totCostDiscInv + totCostDiscNonInv:
		raise Exception("There was an error in calculation")

	return

##-------------------------------##
def measBCR(netBenefits, totalCostsInv, totalCostsInvBase):
        numerator = netBenefits ## I know this isn't really a simplification, however it makes the logic that follow easier to understand
        denominator = totalCostsInv-totalCostsInvBase
        if denominator <= 0 and numerator > 0: ## Need to come up with a better tolerance here to avoid divide by zero error
                bcr = 'Infinity'
        elif (denominator <= 0 and numerator <= 0):
                bcr = "Not Calculable"
        else:
                bcr = numerator/denominator
        return bcr

##-------------------------------##
def measSIR(totalCostsInv, totalCostsNonInv, totalCostsInvBase, totalCostsNonInvBase):
        numerator = (totalCostsNonInvBase-totalCostsNonInv)
        denominator = (totalCostsInvBase-totalCostsInv)
        if denominator <= 0 and numerator > 0: ## Need to come up with a better tolerance here to avoid divide by zero error
                sir = 'Infinity'
        elif denominator <= 0 and numerator <= 0:
                sir = "Not Calculable"
        else:
                sir = numerator/denominator
        return sir

##-------------------------------##
def measAIRR(sir,reinvestRate,studyPeriod):
        if sir == "Not Calculable" or sir == "Infinity" or sir <= 0:
                return "AIRR Not Calculable"
        if sir > 0:
                return (1+reinvestRate)*(sir)**(1/studyPeriod)-1

##-------------------------------##
def measDeltaQ(baselineFlow,altFlow):
	return altFlow - baselineFlow

##-------------------------------##
def measNSPerQ(netSavings, deltaQ):
        if deltaQ != 0:
                return netSavings/deltaQ
        else:
                return "Infinity"

##-------------------------------##
def measNSPerPctQ(netSavings, deltaQ, totQBase):
        if deltaQ != 0 and totQBase != 0:
                return netSavings/(deltaQ/totQBase)
        else:
                return "Infinity"

##-------------------------------##
def measNSElasticity(netSavings,totCosts,deltaQ,totQBase):
        if deltaQ != 0 and totQBase != 0:
                return (netSavings/totCosts)/(deltaQ/totQBase)
        else:
                return "Infinity"

##-------------------------------##
def measIRR(totCosts,totBenefits):
        totFlows = np.subtract(totCosts,totBenefits)
        measIRR = np.irr(totFlows)
        return measIRR

##-------------------------------##
def measPaybackPeriod(totCosts,totBenefits):  ## used for both simple and discounted payback
        dpp = "Infinity"
        for i in range(len(totCosts)):
                if np.sum(totCosts[:i+1])-np.sum(totBenefits[:i+1]) <= 0:
                        dpp = i
                        break ####### Make change on Github
        return dpp
