class SensitivitySummary():
    """
    Represents a sensitivity summary object.
    """
    def __init__(self, bcnObj, varName, diffType, diffVal, diffSign, measure_summaries):
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
        self.nsElasticityQuant = {measure_summary.altID: measure_summary.nsElasticity for measure_summary in measure_summaries}