from django.db import models
from main.models import totalRequiredFlows, totalOptionalFlows


def checkCosts(totReqFlow):
	if totReqFlow.totCostDisc != totReqFlow.totCostDiscInv + totReqFlow.totCostDiscNonInv:
		raise Exception("There was an error in calculation")

	return


def sumCosts(totReqFlow.totCostDisc):
	totalCosts = 0

	studyPeriod = len(totReqFlow.totCostsDisc)
	for i in range(studyPeriod+1):
		totalCosts += totReqFlow.totCostDisc[i]
	return totalCosts

def sumBenefits(totReqFlow.totBenefitsDisc):
	totalBenefits = 0

	studyPeriod = len(totReqFlow.totBenefitsDisc)
	for i in range(studyPeriod + 1):
		totalBenefits += totReqFlow.totBenefitsDisc[i]
	return totalBenefits

def sumInv(totReqFlow.totCostsDisc):
	totalCostsInv = 0

	studyPeriod = len(totReqFlow.totCostsDisc)
	for i in range(studyPeriod + 1):
		totalCostsInv += totReqFlow.totCostsDisc[i]
	return totalCostsInv


def sumNonInv(totReqFlow.totCostsDisc):
    # sum of all non Investment variables
	pass 


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
    		
	return quantSum, quantUnits