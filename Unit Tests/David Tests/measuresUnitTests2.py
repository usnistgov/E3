import numpy as np

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

netBenefits = -301.3405925
totalCostsInv = 431.3043922
totalCostsInvBase = 94.9622353

if abs(measBCR(netBenefits, totalCostsInv, totalCostsInvBase) - (-0.89593465)) < 0.00001:
        print("measBCR-Negative Benefits: Pass")
else:
        print("measBCR-Negative Benefits: Fail")
        print(measBCR(netBenefits, totalCostsInv, totalCostsInvBase))

netBenefits = 4711.424708
totalCostsInv = 431.3043922
totalCostsInvBase = 94.9622353

if abs(measBCR(netBenefits, totalCostsInv, totalCostsInvBase) - 14.00783283) <0.000001:
        print("measBCR-Valid Input: Pass")
else:
        print("measBCR-Valid Input: Fail")
        print(measBCR(netBenefits, totalCostsInv, totalCostsInvBase))

netBenefits = 1000.12343
totalCostsInv = 50.1233243
totalCostsInvBase = 230.102938473

if measBCR(netBenefits, totalCostsInv, totalCostsInvBase) == "Infinity":
        print("measBCR-Negative Denom: Pass")
else:
        print("measBCR-Negative Denom: Fail")
        print(measBCR(netBenefits, totalCostsInv, totalCostsInvBase))

netBenefits = 1000.12343
totalCostsInv = 50
totalCostsInvBase = 50

if measBCR(netBenefits, totalCostsInv, totalCostsInvBase) == "Infinity":
        print("measBCR-Zero Denom: Pass")
else:
        print("measBCR-Zero Denom: Fail")
        print(measBCR(netBenefits, totalCostsInv, totalCostsInvBase))

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

totalCostsInv = 431.3043922
totalCostsNonInv = 1148.990483
totalCostsInvBase = 94.9622353
totalCostsNonInvBase = 1148.990483

if measSIR(totalCostsInv, totalCostsNonInv, totalCostsInvBase, totalCostsNonInvBase) == "Not Calculable":
        print("measBCR-Zero Numerator: Pass")
else:
        print("measBCR-Zero Numerator: Fail")
        print(measSIR(totalCostsInv, totalCostsNonInv, totalCostsInvBase, totalCostsNonInvBase))

totalCostsInv = 431.3043922
totalCostsNonInv = 133.8318721
totalCostsInvBase = 94.9622353
totalCostsNonInvBase = 1148.990483

if measSIR(totalCostsInv, totalCostsNonInv, totalCostsInvBase, totalCostsNonInvBase) == "Infinity":
        print("measBCR-Negative Denom: Pass")
else:
        print("measBCR-Negative Denom: Fail")
        print(measSIR(totalCostsInv, totalCostsNonInv, totalCostsInvBase, totalCostsNonInvBase))

totalCostsInv = 100.23324
totalCostsNonInv = 300.24324
totalCostsInvBase = 200.23434
totalCostsNonInvBase = 550.234324

if abs(measSIR(totalCostsInv, totalCostsNonInv, totalCostsInvBase, totalCostsNonInvBase) - 2.499883341) < 0.0000001:
        print("measBCR-Valid Inputs: Pass")
else:
        print("measBCR-Valid Inputs: Fail")
        print(measSIR(totalCostsInv, totalCostsNonInv, totalCostsInvBase, totalCostsNonInvBase))

totalCostsInv = 100
totalCostsNonInv = 133.8318721
totalCostsInvBase = 100
totalCostsNonInvBase = 1148.990483

if measSIR(totalCostsInv, totalCostsNonInv, totalCostsInvBase, totalCostsNonInvBase) == "Infinity":
        print("measBCR-Zero Denom: Pass")
else:
        print("measBCR-Zero Denom: Fail")
        print(measSIR(totalCostsInv, totalCostsNonInv, totalCostsInvBase, totalCostsNonInvBase))

##-------------------------------##
def measAIRR(sir,reinvestRate,studyPeriod):
        if sir == "Not Calculable" or sir == "Infinity" or sir <= 0:
                return "AIRR Not Calculable"
        if sir > 0:
                return (1+reinvestRate)*(sir)**(1/studyPeriod)-1

sir = "Not Calculable"
reinvestRate = 0.05
studyPeriod = 10

if measAIRR(sir,reinvestRate,studyPeriod) == "AIRR Not Calculable":
        print("measAIRR-Not Calc SIR: Pass")
else:
        print("measAIRR-Not Calc SIR: Fail")
        print(measAIRR(sir,reinvestRate,studyPeriod))

sir = "Infinity"
reinvestRate = 0.05
studyPeriod = 10

if measAIRR(sir,reinvestRate,studyPeriod) == "AIRR Not Calculable":
        print("measAIRR-Infinity SIR: Pass")
else:
        print("measAIRR-Infinity SIR: Fail")
        print(measAIRR(sir,reinvestRate,studyPeriod))

sir = -2.5001
reinvestRate = 0.05
studyPeriod = 10

if measAIRR(sir,reinvestRate,studyPeriod) == "AIRR Not Calculable":
        print("measAIRR-Negative SIR: Pass")
else:
        print("measAIRR-Negative SIR: Fail")
        print(measAIRR(sir,reinvestRate,studyPeriod))

sir = 2.5001
reinvestRate = 0.05
studyPeriod = 10.0

if abs(measAIRR(sir,reinvestRate,studyPeriod) - 0.150760741) < 0.0000001:
        print("measAIRR-Valid Input: Pass")
else:
        print("measAIRR-Valid Input: Fail")
        print(measAIRR(sir,reinvestRate,studyPeriod))
