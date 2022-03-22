class SensitivitySummary():
    """
    Represents a sensitivity summary object.
    """
    def __init__(self, globalVarBool, bcnObj, varName, diffType, diffVal, diffSign, measure_summaries):
        self.globalVarBool = globalVarBool
        self.bcnObj = bcnObj
        self.varName = varName
        self.diffType = diffType
        self.diffVal = diffVal
        self.diffSign = diffSign
        ## self.altOutput = {measure_summaries.altID: measure_summaries for measure_summaries in measure_summaries}
        self.totalBenefits = {measure_summary.altID: measure_summary.totalBenefits for measure_summary in measure_summaries}
        self.totalCosts = {measure_summary.altID: measure_summary.totalCosts for measure_summary in measure_summaries}
        self.totalCostsInv = {measure_summary.altID: measure_summary.totalCostsInv for measure_summary in measure_summaries}
        self.totalCostsNonInv = {measure_summary.altID: measure_summary.totalCostsNonInv for measure_summary in measure_summaries}
        self.totSubtypeFlows = {measure_summary.altID: measure_summary.totSubtypeFlows for measure_summary in measure_summaries}
        self.totTagFlows = {measure_summary.altID: measure_summary.totTagFlows for measure_summary in measure_summaries}
        self.netBenefits = {measure_summary.altID: measure_summary.netBenefits for measure_summary in measure_summaries}
        self.netSavings = {measure_summary.altID: measure_summary.netSavings for measure_summary in measure_summaries}
        self.SIR = {measure_summary.altID: measure_summary.SIR for measure_summary in measure_summaries}
        self.IRR = {measure_summary.altID: measure_summary.IRR for measure_summary in measure_summaries}
        self.AIRR = {measure_summary.altID: measure_summary.AIRR for measure_summary in measure_summaries}
        self.DPP = {measure_summary.altID: measure_summary.DPP for measure_summary in measure_summaries}
        self.SPP = {measure_summary.altID: measure_summary.SPP for measure_summary in measure_summaries}
        self.BCR = {measure_summary.altID: measure_summary.BCR for measure_summary in measure_summaries}
        self.quantSum = {measure_summary.altID: measure_summary.quantSum for measure_summary in measure_summaries}
        self.quantUnits = {measure_summary.altID: measure_summary.quantUnits for measure_summary in measure_summaries}
        self.MARR = {measure_summary.altID: measure_summary.MARR for measure_summary in measure_summaries}
        self.deltaQuant = {measure_summary.altID: measure_summary.deltaQuant for measure_summary in measure_summaries}
        self.nsDeltaQuant = {measure_summary.altID: measure_summary.nsDeltaQuant for measure_summary in measure_summaries}
        self.nsPercQuant = {measure_summary.altID: measure_summary.nsPercQuant for measure_summary in measure_summaries}
        self.nsElasticityQuant = {measure_summary.altID: measure_summary.nsElasticityQuant for measure_summary in measure_summaries}

    ## For testing, has no use in final code
    def __str__(self):
        print("globalVarBool:", self.globalVarBool)
        print("bcnObj:", self.bcnObj)
        print("varName:", self.varName)
        print("diffType:", self.diffType)
        print("diffVal:", self.diffVal)
        print("diffSign:", self.diffSign)
        print("totalBenefits:", self.totalBenefits)
        print("totalCosts:", self.totalCosts)
        print("totalCostsInv:", self.totalCostsInv)
        print("totalCostsNonInv:", self.totalCostsNonInv)
        print("totTagFlows:", self.totTagFlows)
        print("netBenefits:", self.netBenefits)
        print("netSavings:", self.netSavings)
        print("SIR:", self.SIR)
        print("IRR:", self.IRR)
        print("AIRR:", self.AIRR)
        print("SPP:", self.SPP)
        print("DPP:", self.DPP)
        print("BCR:", self.BCR)
        print("quantSum:", self.quantSum)
        print("quantUnits", self.quantUnits)
        print("MARR:", self.MARR)
        print("deltaQuant:", self.deltaQuant)
        print("nsPercQuant:", self.nsPercQuant)
        print("nsDeltaQuant:", self.nsDeltaQuant)
        print("nsElasticityQuant:", self.nsElasticityQuant)
        return "--------------------End of Object--------------------"