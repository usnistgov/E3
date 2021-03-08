from django.db import models
sys.path.insert(1, '/e3_django/main/models')
import (totalRequiredFlows, totalOptionalFlows)

def checkCosts(totReqFlow):
	if totReqFlow.totCostDisc != totReqFlow.totCostDiscInv + totReqFlow.totCostDiscNonInv:
		raise Exception("There was an error in calculation")

	return


def sumCosts(totReqFlow.totCostDisc):
	totalBenefits = 0
	studyPeriod = len(totReqFlow.totBenefitsDisc)
	for i in range(studyPeriod):
		totalBenefits += totReqFlow.totCostDisc[i]
	return totalBenefits

def sumbenefits(totReqFlow.totCostsDisc):
	totalCosts = 0
	studyPeriod = len(totReqFlow.totsCostsDisc)
	for i in range(studyPeriod):
		totalCosts += totReqFlow.totCostsDisc[i]
	return totalCosts

def sumInv(totReqFlow.totCostsDisc):
	totalCostsInv = 0
	studyPeriod = len(totReqFlow.totCostsDisc)
	for i in range(studyPeriod):
		totalCostsInv += totReqFlow.totCostsDisc[i]
	return totalCostsInv


def sumNonInv(totReqFlow.totCostsDisc):
	return 


def netBenefits(totalBenefits, totalCosts, totalBenefitsBase, totalCostsBase):
	netBenefits = 0
	#netBenefits = (ttalBenefits[])

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

def measIRR(altID):
	measIRR = 0
	return measIRR

def measDPP(altID):
	return

def totalQuant(altID, tag):
	quantSum = 0
	return quantSum, quantUnits