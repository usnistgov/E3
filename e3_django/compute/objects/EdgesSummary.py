from decimal import Decimal

def filter_tags(tagged_bcn_dict):
    tagged_bcn_dict_editable = tagged_bcn_dict.copy()
    key_list = list(tagged_bcn_dict_editable.keys())
    key_filter = ["Cost-Direct", "Cost-Indirect", "OMR Recurring", "OMR One-Time", "Positive Recurring",
                  "Positive One-Time", "Negative Recurring", "Negative One-Time", "Response and Recover",
                  "Direct Loss Reduction", "Indirect Loss Reduction", "Fatalities Averted", "NDRB Recurring",
                  "NDRB One-Time"]
    return {key: tagged_bcn_dict_editable[key] for key in key_list if key not in key_filter}


class EdgesSummary():
    """
    Represents aen edges summary object.
    """
    def __init__(self, altID, alternativeSummary, pvExts, fatAvert, npvExts, bcrExts, irrExts, roiExts, nonDisRoiExts,
                 npvNoExts, bcrNoExts, irrNoExts, roiNoExts, nonDisRoiNoExts):
        self.altID = altID
        self.totalDirectCosts = alternativeSummary.totSubtypeFlows["Cost-Direct"] if alternativeSummary.totTagFlows["Cost-Direct"] else Decimal(0)
        self.totalIndirectCosts = alternativeSummary.totSubtypeFlows["Cost-Indirect"] if alternativeSummary.totTagFlows["Cost-Indirect"] else Decimal(0)
        self.omrRecur = alternativeSummary.totTagFlows["OMR Recurring"] if alternativeSummary.totTagFlows["OMR Recurring"] else Decimal(0)
        self.omrOneTime = alternativeSummary.totTagFlows["OMR One-Time"] if alternativeSummary.totTagFlows["OMR One-Time"] else Decimal(0)
        self.posExtRecur = alternativeSummary.totTagFlows["Positive Recurring"] if alternativeSummary.totTagFlows["Positive Recurring"] else Decimal(0)
        self.posExtOneTime = alternativeSummary.totTagFlows["Positive One-Time"] if alternativeSummary.totTagFlows["Positive One-Time"] else Decimal(0)
        self.negExtRecur = alternativeSummary.totTagFlows["Negative Recurring"] if alternativeSummary.totTagFlows["Negative Recurring"] else Decimal(0)
        self.negExtOneTime = alternativeSummary.totTagFlows["Negative One-Time"] if alternativeSummary.totTagFlows["Negative One-Time"] else Decimal(0)
        self.pvBens = alternativeSummary.totalBenefits
        self.pvCosts = alternativeSummary.totalCosts
        self.pvExts = pvExts
        self.respRec = alternativeSummary.totTagFlows["Response and Recovery"] if alternativeSummary.totTagFlows["Response and Recovery"] else Decimal(0)
        self.dirLossRed = alternativeSummary.totTagFlows["Direct Loss Reduction"] if alternativeSummary.totTagFlows["Direct Loss Reduction"] else Decimal(0)
        self.indirLossRed = alternativeSummary.totTagFlows["Indirect Loss Reduction"] if alternativeSummary.totTagFlows["Indirect Loss Reduction"] else Decimal(0)
        self.fatAvert = fatAvert
        self.valFatAvert = alternativeSummary.totTagFlows["Fatalities Averted"] if alternativeSummary.totTagFlows["Fatalities Averted"] else Decimal(0)
        self.ndrbRecur = alternativeSummary.totTagFlows["NDRB Recurring"] if alternativeSummary.totTagFlows["NDRB Recurring"] else Decimal(0)
        self.ndrbOneTime = alternativeSummary.totTagFlows["NDRB One-Time"] if alternativeSummary.totTagFlows["NDRB One-Time"] else Decimal(0)
        self.npvExts = npvExts
        self.bcrExts = bcrExts
        self.irrExts = irrExts
        self.roiExts = roiExts
        self.nonDisRoiExts = nonDisRoiExts
        self.npvNoExts = npvNoExts
        self.bcrNoExts = bcrNoExts
        self.irrNoExts = irrNoExts
        self.roiNoExts = roiNoExts
        self.nonDisRoiNoExts = nonDisRoiNoExts
        self.otherTags = filter_tags(alternativeSummary.totTagFlows)

    ## Allows for object to be directly printed out to console when testing, has no use in final code
    def __str__(self):
        print("altID:", self.altID)
        return "--------------------End of Object--------------------"
