import numpy as np
import measures

## Build objects for the test
class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

class  TotalRequiredFlows:
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self,altID,baselineBool,sensBool,uncBool,totCostsNonDisc,totCostsDisc,totCostsNonDiscInv,totCostsDiscInv,totCostsNonDiscNonInv,
                 totCostsDiscNonInv,totBenefitsNonDisc,totBenefitsDisc,totCostsDir,totCostsInd,totCostsExt,totCostsDirDisc,totCostsIndDisc,
                 totCostsExtDisc,totBenefitsDir,totBenefitsInd,totBenefitsExt,totBenefitsDirDisc,totBenefitsIndDisc,totBenefitsExtDisc):
        self._registry.append(self)
        self.altID = altID
        self.baselineBool = baselineBool
        self.sensBool = sensBool
        self.uncBool = uncBool
        self.totCostsNonDisc = totCostsNonDisc
        self.totCostsDisc = totCostsDisc
        self.totCostsNonDiscInv = totCostsNonDiscInv
        self.totCostsDiscInv = totCostsDiscInv
        self.totCostsNonDiscNonInv = totCostsNonDiscNonInv
        self.totCostsDiscNonInv = totCostsDiscNonInv
        self.totBenefitsNonDisc = totBenefitsNonDisc
        self.totBenefitsDisc = totBenefitsDisc
        self.totCostsDir = totCostsDir
        self.totCostsInd = totCostsInd
        self.totCostsExt = totCostsExt
        self.totCostsDirDisc = totCostsDirDisc
        self.totCostsIndDisc = totCostsIndDisc
        self.totCostsExtDisc = totCostsExtDisc
        self.totBenefitsDir = totBenefitsDir
        self.totBenefitsInd = totBenefitsInd
        self.totBenefitsExt = totBenefitsExt
        self.totBenefitsDirDisc = totBenefitsDirDisc
        self.totBenefitsIndDisc = totBenefitsIndDisc
        self.totBenefitsExtDisc = totBenefitsExtDisc

class TotalOptionalFlows:
    __metaclass__ = IterRegistry
    _registry = []

    def __init__(self,altID,sensBool,uncBool,bcnType,bcnSubtype,bcnTag,totTagFlow,totTagQ,quantUnits):
        self._registry.append(self)
        self.altID = altID
        self.sensBool = sensBool
        self.uncBool = uncBool
        self.bcnType = bcnType
        self.bcnSubtype = bcnSubtype
        self.bcnTag = bcnTag
        self.totTagFlow = totTagFlow
        self.totTagQ = totTagQ
        self.quantUnits = quantUnits

altID = 0
baselineBool = True
sensBool = False
uncBool = False
totCostsNonDisc = [0,294.0905,101.7588758,110.0522241,119.0214804,128.721731,139.2125521,150.5583751,162.8288827,176.0994366,57.11820738]
totCostsDisc = [0,285.5247573,95.9175,100.713375,105.7490438,111.0364959,116.5883207,122.4177368,128.5386236,134.9655548,42.50131054]
totCostsNonDiscInv = [0,200,0,0,0,0,0,0,0,0,-133.3333333]
totCostsDiscInv = [0,194.1747573,0,0,0,0,0,0,0,0,-99.21252199]
totCostsNonDiscNonInv = [0,94.0905,101.7588758,110.0522241,119.0214804,128.721731,139.2125521,150.5583751,162.8288827,176.0994366,190.4515407]
totCostsDiscNonInv = [0,91.35,95.9175,100.713375,105.7490438,111.0364959,116.5883207,122.4177368,128.5386236,134.9655548,141.7138325]
totBenefitsNonDisc = [0,0,0,0,0,0,125,0,0,0,0]
totBenefitsDisc = [0,0,0,0,0,0,104.6855321,0,0,0,0]
totCostsDir = [0,200,0,0,0,0,0,0,0,0,-133.3333333]
totCostsInd = [0,94.0905,101.7588758,110.0522241,119.0214804,128.721731,139.2125521,150.5583751,162.8288827,176.0994366,190.4515407]
totCostsExt = [0,0,0,0,0,0,0,0,0,0,0]
totCostsDirDisc = [0,194.1747573,0,0,0,0,0,0,0,0,-99.21252199]
totCostsIndDisc = [0,91.35,95.9175,100.713375,105.7490438,111.0364959,116.5883207,122.4177368,128.5386236,134.9655548,141.7138325]
totCostsExtDisc = [0,0,0,0,0,0,0,0,0,0,0]
totBenefitsDir = [0,0,0,0,0,0,0,0,0,0,0]
totBenefitsInd = [0,0,0,0,0,0,125,0,0,0,0]
totBenefitsExt = [0,0,0,0,0,0,0,0,0,0,0]
totBenefitsDirDisc = [0,0,0,0,0,0,0,0,0,0,0]
totBenefitsIndDisc = [0,0,0,0,0,0,104.6855321,0,0,0,0]
totBenefitsExtDisc = [0,0,0,0,0,0,0,0,0,0,0]

TotalRequiredFlows(altID,baselineBool,sensBool,uncBool,totCostsNonDisc,totCostsDisc,totCostsNonDiscInv,totCostsDiscInv,totCostsNonDiscNonInv,
                 totCostsDiscNonInv,totBenefitsNonDisc,totBenefitsDisc,totCostsDir,totCostsInd,totCostsExt,totCostsDirDisc,totCostsIndDisc,
                 totCostsExtDisc,totBenefitsDir,totBenefitsInd,totBenefitsExt,totBenefitsDirDisc,totBenefitsIndDisc,totBenefitsExtDisc)

altID = 1
baselineBool = False
sensBool = False
uncBool = False
totCostsNonDisc = [0,94.0905,101.7588758,110.0522241,119.0214804,628.721731,139.2125521,150.5583751,162.8288827,176.0994366,190.4515407]
totCostsDisc = [0,91.35,95.9175,100.713375,105.7490438,542.3408881,116.5883207,122.4177368,128.5386236,134.9655548,141.7138325]
totCostsNonDiscInv = [0,0,0,0,0,500,0,0,0,0,0]
totCostsDiscInv = [0,0,0,0,0,431.3043922,0,0,0,0,0]
totCostsNonDiscNonInv = [0,94.0905,101.7588758,110.0522241,119.0214804,128.721731,139.2125521,150.5583751,162.8288827,176.0994366,190.4515407]
totCostsDiscNonInv = [0,91.35,95.9175,100.713375,105.7490438,111.0364959,116.5883207,122.4177368,128.5386236,134.9655548,141.7138325]
totBenefitsNonDisc = [0.9,0.88173,31.46683088,0.846295114,32.66847652,0.812284282,32.63197218,0.779640275,32.79762982,0,32.14167722]
totBenefitsDisc = [0.9,0.856048544,29.66050606,0.774479915,29.02551827,0.700683557,27.32876296,0.633918889,25.89075184,0,23.91642643]
totCostsDir = [0,0,0,0,0,0,0,0,0,0,0]
totCostsInd = [0,94.0905,101.7588758,110.0522241,119.0214804,128.721731,139.2125521,150.5583751,162.8288827,176.0994366,190.4515407]
totCostsExt = [0,0,0,0,0,500,0,0,0,0,0]
totCostsDirDisc = [0,0,0,0,0,0,0,0,0,0,0]
totCostsIndDisc = [0,91.35,95.9175,100.713375,105.7490438,111.0364959,116.5883207,122.4177368,128.5386236,134.9655548,141.7138325]
totCostsExtDisc = [0,0,0,0,0,431.3043922,0,0,0,0,0]
totBenefitsDir = [0,0,30.603,0,31.8393612,0,31.83617726,0,32.79762982,0,32.14167722]
totBenefitsInd = [0.9,0.88173,0.863830881,0.846295114,0.829115323,0.812284282,0.795794911,0.779640275,0,0,0]
totBenefitsExt = [
0,0,0,0,0,0,0,0,0,0,0]
totBenefitsDirDisc = [0,0,28.84626261,0,28.28886004,0,26.66229725,0,25.89075184,0,23.91642643]
totBenefitsIndDisc = [0.9,0.856048544,0.814243455,0.774479915,0.736658226,0.700683557,0.66646571,0.633918889,0,0,0]
totBenefitsExtDisc = [0,0,0,0,0,0,0,0,0,0,0]

TotalRequiredFlows(altID,baselineBool,sensBool,uncBool,totCostsNonDisc,totCostsDisc,totCostsNonDiscInv,totCostsDiscInv,totCostsNonDiscNonInv,
                 totCostsDiscNonInv,totBenefitsNonDisc,totBenefitsDisc,totCostsDir,totCostsInd,totCostsExt,totCostsDirDisc,totCostsIndDisc,
                 totCostsExtDisc,totBenefitsDir,totBenefitsInd,totBenefitsExt,totBenefitsDirDisc,totBenefitsIndDisc,totBenefitsExtDisc)

altID = 2
baselineBool = False
sensBool = False
uncBool = False
totCostsNonDisc = [50,0,0,0,52.0302005,500,0,0,54.14283528,0,-6.903888284]
totCostsDisc = [50,0,0,0,46.22815924,431.3043922,0,0,42.74085414,0,-5.137141261]
totCostsNonDiscInv = [0,0,0,0,0,500,0,0,0,0,0]
totCostsDiscInv = [0,0,0,0,0,431.3043922,0,0,0,0,0]
totCostsNonDiscNonInv = [50,0,0,0,52.0302005,0,0,0,54.14283528,0,-6.903888284]
totCostsDiscNonInv = [50,0,0,0,46.22815924,0,0,0,42.74085414,0,-5.137141261]
totBenefitsNonDisc = [0.9,0.88173,0.863830881,1172.049055,1183.743903,1148.239628,1217.06878,0.779640275,0,0,0]
totBenefitsDisc = [0.9,0.856048544,0.814243455,1072.590917,1051.741126,990.4815899,1019.275942,0.633918889,0,0,0]
totCostsDir = [
0,0,0,0,0,0,0,0,0,0,0]
totCostsInd = [50,0,0,0,52.0302005,0,0,0,54.14283528,0,-6.903888284]
totCostsExt = [0,0,0,0,0,500,0,0,0,0,0]
totCostsDirDisc = [0,0,0,0,0,0,0,0,0,0,0]
totCostsIndDisc = [50,0,0,0,46.22815924,0,0,0,42.74085414,0,-5.137141261]
totCostsExtDisc = [0,0,0,0,0,431.3043922,0,0,0,0,0]
totBenefitsDir = [0,0,0,0,0,0,0,0,0,0,0]
totBenefitsInd = [0.9,0.88173,0.863830881,1172.049055,1183.743903,1148.239628,1217.06878,0.779640275,0,0,0]
totBenefitsExt = [0,0,0,0,0,0,0,0,0,0,0]
totBenefitsDirDisc = [0,0,0,0,0,0,0,0,0,0,0]
totBenefitsIndDisc = [0.9,0.856048544,0.814243455,1072.590917,1051.741126,990.4815899,1019.275942,0.633918889,0,0,0]
totBenefitsExtDisc = [0,0,0,0,0,0,0,0,0,0,0]

TotalRequiredFlows(altID,baselineBool,sensBool,uncBool,totCostsNonDisc,totCostsDisc,totCostsNonDiscInv,totCostsDiscInv,totCostsNonDiscNonInv,
                 totCostsDiscNonInv,totBenefitsNonDisc,totBenefitsDisc,totCostsDir,totCostsInd,totCostsExt,totCostsDirDisc,totCostsIndDisc,
                 totCostsExtDisc,totBenefitsDir,totBenefitsInd,totBenefitsExt,totBenefitsDirDisc,totBenefitsIndDisc,totBenefitsExtDisc)

altID = 0
sensBool = False
uncBool = False
bcnType = "Benefit"
bcnSubtype = "Direct"
bcnTag = "Tag 1"
totTagFlow = [0,194.1747573,0,0,0,0,0,0,0,0,-99.21252199]
totTagQ = [0,100,0,0,0,0,0,0,0,0,0]
quantUnits = "m^3"

TotalOptionalFlows(altID,sensBool,uncBool,bcnType,bcnSubtype,bcnTag,totTagFlow,totTagQ,quantUnits)

altID = 1
sensBool = False
uncBool = False
bcnType = "Benefit"
bcnSubtype = "Direct"
bcnTag = "Tag 1"
totTagFlow = [0,0,28.84626261,0,28.28886004,0,26.66229725,0,25.89075184,0,23.91642643]
totTagQ = [0,0,30.603,0,31.8393612,0,31.83617726,0,32.79762982,0,32.14167722]
quantUnits = "m^3"

TotalOptionalFlows(altID,sensBool,uncBool,bcnType,bcnSubtype,bcnTag,totTagFlow,totTagQ,quantUnits)

altID = 1
sensBool = False
uncBool = False
bcnType = "Benefit"
bcnSubtype = "Indirect"
bcnTag = "Tag 1"
totTagFlow = [0.9,0.856048544,0.814243455,0.774479915,0.736658226,0.700683557,0.66646571,0.633918889,0,0,0]
totTagQ = [90,87.3,84.681,82.14057,79.6763529,77.28606231,74.96748044,72.71845603,0,0,0]
quantUnits = "m^2"

TotalOptionalFlows(altID,sensBool,uncBool,bcnType,bcnSubtype,bcnTag,totTagFlow,totTagQ,quantUnits)

altID = 1
sensBool = False
uncBool = False
bcnType = "Benefit"
bcnSubtype = "Indirect"
bcnTag = "Tag 3"
totTagFlow = [0,0,0,0,0,0,0,0,0,0,0]
totTagQ = [100,100,100,100,100,100,100,100,100,100,100]
quantUnits = "m"

TotalOptionalFlows(altID,sensBool,uncBool,bcnType,bcnSubtype,bcnTag,totTagFlow,totTagQ,quantUnits)

altID = 2
sensBool = False
uncBool = False
bcnType = "Benefit"
bcnSubtype = "Indirect"
bcnTag = "Tag 1"
totTagFlow = [0.9,0.856048544,0.814243455,0.774479915,0.736658226,0.700683557,0.66646571,0.633918889,0,0,0]
totTagQ = [90,87.3,84.681,82.14057,79.6763529,77.28606231,74.96748044,72.71845603,0,0,0]
quantUnits = "m^3"

TotalOptionalFlows(altID,sensBool,uncBool,bcnType,bcnSubtype,bcnTag,totTagFlow,totTagQ,quantUnits)

altID = 2
sensBool = False
uncBool = False
bcnType = "Cost"
bcnSubtype = "Indirect"
bcnTag = "Tag 2"
totTagFlow = [50,0,0,0,46.22815924,0,0,0,42.74085414,0,-5.137141261]
totTagQ = [100,0,0,0,100,0,0,0,100,0,-12.5]
quantUnits = "m^2"

TotalOptionalFlows(altID,sensBool,uncBool,bcnType,bcnSubtype,bcnTag,totTagFlow,totTagQ,quantUnits)

altID = 2
sensBool = False
uncBool = False
bcnType = "Benefit"
bcnSubtype = "Indirect"
bcnTag = "Tag 3"
totTagFlow = [0,0,0,0,0,0,0,0,0,0,0]
totTagQ = [100,100,100,100,100,100,100,100,100,100,100]
quantUnits = "m"

TotalOptionalFlows(altID,sensBool,uncBool,bcnType,bcnSubtype,bcnTag,totTagFlow,totTagQ,quantUnits)

## Begin testing
def calcBaselineMeas(baselineTotFlows,irrBoolean):  ## Update main with irrBoolean input
    totFlows = np.subtract(baselineTotFlows.totCostsDisc,baselineTotFlows.totBenefitsDisc)
    totFlowsNonDisc = np.subtract(baselineTotFlows.totCostsNonDisc,baselineTotFlows.totBenefitsNonDisc)
    totCosts = baselineTotFlows.totCostsDisc
    totBens = baselineTotFlows.totBenefitsDisc
    totCostsInv = baselineTotFlows.totCostsDiscInv
    totCostsNonInv = baselineTotFlows.totCostsDiscNonInv
    baselineFlowList = [np.sum(totFlows),np.sum(totCosts),np.sum(totBens),np.sum(totCostsInv),np.sum(totCostsNonInv)]

    totalCostsBase = measures.sumCosts(totCosts)
    totalBenefitsBase = measures.sumBenefits(totBens)
    totalInvBase = measures.sumInv(totCostsInv)
    totalNonInvBase = measures.sumNonInv(totCostsNonInv)
    if irrBoolean == True:
        irr = measures.measIRR(totFlowsNonDisc)
    else:
        irr = None
    dpp = measures.measPaybackPeriod(totCosts,totBens) 
    spp = measures.measPaybackPeriod(baselineTotFlows.totCostsNonDisc,baselineTotFlows.totBenefitsNonDisc) ## Only call to these two attributes

    baselineMeasList = [baselineID, totalBenefitsBase, totalCostsBase, totalInvBase, totalNonInvBase, None, None, irr,
                        None, dpp, spp, None]

    return baselineFlowList, baselineMeasList

for totRFlow in TotalRequiredFlows._registry:
    if totRFlow.baselineBool == True:
        baselineID = totRFlow.altID
        baselineAlt = totRFlow
        break
irrBoolean = False

baselineFlowList, baselineMeasList = calcBaselineMeas(baselineAlt,irrBoolean)

print("baselineFlowList:", baselineFlowList)
print("baselineMeasList:", baselineMeasList)
##--------------------------------------##

def calcBaselineTagMeas(baselineTagList,altID,tag,flowDisc,totTagQ,units):
    if altID == baselineID and tag not in baselineTagList: ## Add new tags to baselineTagList
        baselineTagList.append([tag,flowDisc,totTagQ,units])
    elif altID == baselineID and tag in baselineTagList:
        tagIndex = baselineTagList.index(tag)
        baselineTagList[i][1] = np.add(flowDisc,baselineTagList[i][1])
        baselineTagList[i][2] = np.add(totTagQ,baselineTagList[i][2])

    for baselineTag in baselineTagList:
        baselineTag[1] = np.sum(baselineTag[1])
        baselineTag[2] = np.sum(baselineTag[2])
    return baselineTagList ## Update Main

baselineTagList = []
altID = baselineID
for totOptFlow in TotalOptionalFlows._registry:
    if totOptFlow.altID == baselineID:
        baselineOptFLow = totOptFlow
        break

tag = baselineOptFLow.bcnTag
totTagFlow = baselineOptFLow.totTagFlow
totTagQ = baselineOptFLow.totTagQ
quantUnits = baselineOptFLow.quantUnits
baselineTagList = calcBaselineTagMeas(baselineTagList,baselineID,tag,totTagFlow,totTagQ,quantUnits)
print("baselineTagList:", baselineTagList)
##--------------------------------------##

def quantList(baselineTagList):
    quantSum = []
    quantUnits = []
    for i in range(len(baselineTagList)):
        quantSum.append([baselineTagList[i][0],np.sum(baselineTagList[i][2])])
        quantUnits.append([baselineTagList[i][0],baselineTagList[i][3]])

    return quantSum, quantUnits

quantSum, quantUnits = quantList(baselineTagList)

print("quantSum:", quantSum)
print("quantUnits:", quantUnits)

##---------------------------------------##
def calcAltMeas(altID,irrBoolean,baselineFlowList,reinvestRate,studyPeriod,altTotFlows):
## Loop through remainder of total Required Flows objects and calculate their measures.
        totFlows = np.subtract(altTotFlows.totCostsDisc,altTotFlows.totBenefitsDisc)
        totFlowsNonDisc = np.subtract(altTotFlows.totCostsNonDisc,altTotFlows.totBenefitsNonDisc)
        totCostFlows = altTotFlows.totCostsDisc
        totBenFlows = altTotFlows.totBenefitsDisc
        totCostInvFlows = altTotFlows.totCostsDiscInv
        totCostNonInvFlows = altTotFlows.totCostsDiscNonInv
    
        totalCosts = measures.sumCosts(totCostFlows)
        totalBenefits = measures.sumBenefits(totBenFlows)
        totalCostsInv = measures.sumInv(totCostInvFlows)
        totalCostsNonInv = measures.sumNonInv(totCostNonInvFlows)
        if irrBoolean == True:
             irr = measures.measIRR(totFlowsNonDisc)
        else:
             irr = None
        netBenefits = measures.netBenefits(totalBenefits,totalCosts,baselineFlowList[2],baselineFlowList[1])
        netSavings = measures.netSavings(totalCosts,baselineFlowList[1])
        bcr = measures.measBCR(netBenefits,totalCostsInv,baselineFlowList[3])
        sir = measures.measSIR(totalCostsInv,totalCostsNonInv,baselineFlowList[3],baselineFlowList[4])
        airr = measures.measAIRR(sir,reinvestRate,studyPeriod)
        dpp = measures.measPaybackPeriod(totCostFlows,totBenFlows)
        spp = measures.measPaybackPeriod(altTotFlows.totCostsNonDisc,altTotFlows.totBenefitsNonDisc)

        altMeasList = [altID, totalBenefits, totalCosts, totalCostsInv, totalCostsNonInv, netBenefits, netSavings, sir, irr, airr,
                       dpp, spp, bcr]
            
        return altMeasList
altID = 1
for totReqFlow in TotalRequiredFlows._registry:
    if totReqFlow.altID == altID:
        totRFlow = totReqFlow
        break
reinvestRate = 0.05
studyPeriod = 10
altMeasList = calcAltMeas(altID,irrBoolean,baselineFlowList,reinvestRate,studyPeriod,totRFlow)

print("altMeasList:", altMeasList)

##---------------------------------##
def calcAltTagMeas(totOptFlowsList,altMeasList,baselineTagList):
    altTagList = []
    altTagFlowList = []
    quantMeasList = []
    deltaQuant = []
    nsDeltaQuant = []
    nsPerQuant = []
    nsPerPctQuant = []
    nsElasticityQuant = []
    for totOptFlow in totOptFlowsList:
        if altID == totOptFlow.altID:
            tag = totOptFlow.bcnTag
            totalTagFlow = totOptFlow.totTagFlow
            totTagQ = totOptFlow.totTagQ
            quantUnits = totOptFlow.quantUnits
            if tag not in altTagList: ## Add new tags to baselineTagList
                altTagList.append(tag)
                altTagFlowList.append([tag,totalTagFlow,totTagQ,quantUnits])
            elif tag in altTagList:
                tagIndex = altTagList.index(tag)  ## If tag exists, add the new values to the previous entries in baselineTagList. These are used for Total Quantity Flows outputs
                altTagFlowList[tagIndex][1] = np.add(totalTagFlow,altTagFlowList[tagIndex][1])
                altTagFlowList[tagIndex][2] = np.add(totTagQ,altTagFlowList[tagIndex][2])

    for altTag in altTagFlowList:
        altTag[1] = np.sum(altTag[1])
        altTag[2] = np.sum(altTag[2])

    for baselineTag in baselineTagList:
        for altTag in altTagFlowList:
            if altTag[0] not in baselineTag:
                deltaQ = altTag[2]
                deltaQuant.append([altTag[0],deltaQ])
                nsPerQuant.append([altTag[0],measures.measNSPerQ(altMeasList[6],baselineTag[2])])
                nsPerPctQuant.append([altTag[0],"Infinite"])
                nsElasticityQuant.append([altTag[0],"Infinite"])
            elif altTag[0] == baselineTag[0]:
                deltaQ = measures.measDeltaQ(baselineTag[2],np.sum(altTag[2]))
                deltaQuant.append([altTag[0],deltaQ])
                nsPerQuant.append([altTag[0],measures.measNSPerQ(altMeasList[6],deltaQ)])
                nsPerPctQuant.append([altTag[0],measures.measNSPerPctQ(altMeasList[6],deltaQ,baselineTag[2])])
                nsElasticityQuant.append([altTag[0],measures.measNSElasticity(altMeasList[6],altMeasList[2],deltaQ,baselineTag[2])])
                
    return [deltaQuant,nsPerQuant,nsPerPctQuant,nsElasticityQuant]

totOptFlowsList = TotalOptionalFlows._registry
altTagMeasList = calcAltTagMeas(totOptFlowsList,altMeasList,baselineTagList)

print("altTagMeasList:",altTagMeasList)
