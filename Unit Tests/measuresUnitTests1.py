import numpy as np

##-------------------------------##
def sumCosts(totCostDisc):
	return np.sum(totCostDisc)

totCostDisc = [0,91.35,95.9175,100.713375,105.7490438,542.3408881,116.5883207,122.4177368,128.5386236,134.9655548,141.7138325]

if abs(sumCosts(totCostDisc) - 1580.294875) < 0.000001:
    print("sumCosts: Pass")
else:
    print("sumCosts: Fail")
    print(sumCosts(totCostDisc))

##-------------------------------##
def sumBenefits(totBenefitsDisc):
	return np.sum(totBenefitsDisc)

totBenefitsDisc = [0.9,0.856048544,29.66050606,0.774479915,29.02551827,0.700683557,27.32876296,0.633918889,25.89075184,0,23.91642643]

if abs(sumBenefits(totBenefitsDisc) - 139.6870965) < 0.000001:
    print("sumBenefits: Pass")
else:
    print("sumBenefits: Fail")
    print(sumBenefits(totBenefitsDisc))

##-------------------------------##
def sumInv(totCostsInvDisc):
	return np.sum(totCostsInvDisc)

totCostsInvDisc = [0,194.1747573,0,0,0,0,0,0,0,0,-99.21252199]

if abs(sumInv(totCostsInvDisc) - 94.9622353) < 0.000001:
    print("sumInv: Pass")
else:
    print("sumInv: Fail")
    print(sumInv(totCostsInvDisc))

##-------------------------------##
def sumNonInv(totCostsNonInvDisc):
	return np.sum(totCostsNonInvDisc)

totCostsNonInvDisc = [0,91.35,95.9175,100.713375,105.7490438,111.0364959,116.5883207,122.4177368,128.5386236,134.9655548,141.7138325]

if abs(sumNonInv(totCostsNonInvDisc) - 1148.990483) < 0.000001:
    print("sumNonInv: Pass")
else:
    print("sumNonInv: Fail")
    print(sumNonInv(totCostsNonInvDisc))
    
##-------------------------------##
def netBenefits(totalBenefits, totalCosts, totalBenefitsBase, totalCostsBase):
	return (totalBenefits-totalBenefitsBase)-(totalCosts-totalCostsBase)

totalBenefits = 4137.293786
totalCosts = 565.1362643
totalBenefitsBase = 104.6855321
totalCostsBase = 1243.952718

if abs(netBenefits(totalBenefits, totalCosts, totalBenefitsBase, totalCostsBase) - 4711.424708) < 0.000001:
    print("netBenefits: Pass")
else:
    print("netBenefits: Fail")
    print(netBenefits(totalBenefits, totalCosts, totalBenefitsBase, totalCostsBase))

##-------------------------------##
def netSavings(totalCosts, totalCostsBase):
	return (totalCostsBase - totalCosts)

totalCostsBase = 1243.952718
totalCosts = 565.1362643

if abs(netSavings(totalCosts, totalCostsBase) - 678.8164541) < 0.000001:
    print("netSavings: Pass")
else:
    print("netSavings: Fail")
    print(netSavings(totalCosts, totalCostsBase))

##-------------------------------##
def checkCosts(totCostDisc,totCostDiscInv,totCostDiscNonInv):
	## Should be run after sumCosts through sumBenefits
	if totCostDisc != totCostDiscInv + totCostDiscNonInv:
		raise Exception("There was an error in calculation")

	return

totCostDisc = 124
totCostDiscInv = 90.5
totCostDiscNonInv = 33.5

checkCosts(totCostDisc,totCostDiscInv,totCostDiscNonInv)
if True:
    print("checkCosts-Valid Inputs: Pass")

totCostDiscNonInv = 33

checkCosts(totCostDisc,totCostDiscInv,totCostDiscNonInv)

