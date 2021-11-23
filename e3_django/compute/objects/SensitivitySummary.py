class SensitivitySummary:
    """
    Represents a sensitivity summary object.
    """
    def __init__(self, sensitivity_id, measure_summary):
        # Alternative ID
        self.altID = measure_summary.altID
        # Sensitivity ID
        self.sensID = sensitivity_id
        self.totalBenefits = measure_summary.totalBenefits
        self.totalCosts = measure_summary.totalCosts
        self.totalCostsInv = measure_summary.totalCostsInv
        self.totalCostsNonInv = measure_summary.totalCostsNonInv
        self.totTagFlows = measure_summary.totTagFlows
        self.netBenefits = measure_summary.netBenefits
        self.netSavings = measure_summary.netSavings
        self.SIR = measure_summary.SIR
        self.IRR = measure_summary.IRR
        self.AIRR = measure_summary.AIRR
        self.DPP = measure_summary.DPP
        self.SPP = measure_summary.SPP
        self.BCR = measure_summary.BCR
        self.quantSum = measure_summary.quantSum
        self.quantUnits = measure_summary.quantUnits
        self.MARR = measure_summary.MARR
        self.deltaQuant = measure_summary.deltaQuant
        self.nsDeltaQuant = measure_summary.nsDeltaQuant
        self.nsPercQuant = measure_summary.nsPercQuant
        self.nsElasticityQuant = measure_summary.nsElasticityQuant