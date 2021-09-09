import numpy as np

##-------------------------------##
def measDeltaQ(baselineFlow,altFlow):
	return altFlow - baselineFlow

baselineFlow = 94.9622353
altFlow = 139.6870965

if abs(measDeltaQ(baselineFlow,altFlow)-44.72486118) < 0.00001:
        print("measDeltaQ: Pass")
else:
        print("measDeltaQ: Fail")
        print(measDeltaQ(baselineFlow,altFlow))

##-------------------------------##
def measNSPerQ(netSavings, deltaQ):
        if deltaQ != 0:
                return netSavings/deltaQ
        else:
                return "Infinity"

netSavings = 678.8164541
deltaQ = 287.5

if abs(measNSPerQ(netSavings,deltaQ)-2.36110071) < 0.00001:
        print("measNSPerQ: Pass")
else:
        print("measNSPerQ: Fail")
        print(measNSPerQ(netSavings,deltaQ))

##-------------------------------##
def measNSPerPctQ(netSavings, deltaQ, totalQBase):
        if deltaQ != 0 and totQBase != 0:
                return netSavings/(deltaQ/totQBase)
        else:
                return "Infinity"

netSavings = 678.8164541
deltaQ = 548.7699217
totQBase = 100

if abs(measNSPerPctQ(netSavings,deltaQ,totQBase)-123.6978244) < 0.00001:
        print("measNSPerPctQ: Pass")
else:
        print("measNSPerPctQ: Fail")
        print(measNSPerPctQ(netSavings,deltaQ,totQBase))
        
##-------------------------------##
def measNSElasticity(netSavings,totCosts,deltaQ,totQBase):
        if deltaQ != 0 and totQBase != 0:
                return (netSavings/totCosts)/(deltaQ/totQBase)
        else:
                return "Infinity"

netSavings = 678.8164541
totCosts = 1243.952718
deltaQ = 548.7699217
totQBase = 100

if abs(measNSElasticity(netSavings,totCosts,deltaQ,totQBase)-0.09943933) < 0.00001:
        print("measNSPerPctQ: Pass")
else:
        print("measNSPerPctQ: Fail")
        print(measNSElasticity(netSavings,totCosts,deltaQ,totQBase))

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

totCosts = [100,50,25,10]
totBenefits = [50,50,100,100]

if measPaybackPeriod(totCosts,totBenefits) == 2:
        print("measPaybackPeriod: Pass")
else:
        print("measPaybackPeriod: Fail")
        print(measPaybackPeriod(totCosts,totBenefits))
