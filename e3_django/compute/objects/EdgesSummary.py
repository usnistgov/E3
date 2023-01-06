from decimal import Decimal

def filter_tags(tagged_bcn_dict, altID):
    """
    Filters tags out for the otherTags variable

    :param tagged_bcn_dict: The dictionary containing tagged BCNs
    :param altID: Current alternatives alt_id
    :return: Dictionary of tagged BCNs that are not represented by name in the EdgesSummary object
    """
    tagged_bcn_dict_editable = tagged_bcn_dict.copy()
    key_list = list(tagged_bcn_dict_editable.keys())
    key_filter = ["Cost-Direct", "Cost-Indirect", "OMR Recurring", "OMR One-Time", "Positive Recurring",
                  "Positive One-Time", "Negative Recurring", "Negative One-Time", "Response and Recovery",
                  "Direct Loss Reduction", "Indirect Loss Reduction", "Fatalities Averted", "NDRB Recurring",
                  "NDRB One-Time"]

    return {key: tagged_bcn_dict_editable[key] for key in key_list if key not in key_filter}


class EdgesSummary():
    """
    Represents an edges summary object.
    """
    def __init__(self, altID, alternativeSummary, pvExts, fatAvert, roiExts, nonDisRoiExts, npvNoExts, bcrNoExts,
                 irrNoExts, roiNoExts, nonDisRoiNoExts):
        self.altID = altID
        self.totalDirectCosts = alternativeSummary.totSubtypeFlows["Cost-Direct"] if alternativeSummary.totSubtypeFlows["Cost-Direct"] else Decimal(0)
        self.totalIndirectCosts = alternativeSummary.totSubtypeFlows["Cost-Indirect"] if alternativeSummary.totSubtypeFlows["Cost-Indirect"] else Decimal(0)
        self.omrRecur = alternativeSummary.totTagFlows["OMR Recurring"] if "OMR Recurring" in alternativeSummary.totTagFlows else Decimal(0)
        self.omrOneTime = alternativeSummary.totTagFlows["OMR One-Time"] if "OMR One-Time" in alternativeSummary.totTagFlows else Decimal(0)
        self.posExtRecur = alternativeSummary.totTagFlows["Positive Recurring"] if "Positive Recurring" in alternativeSummary.totTagFlows else Decimal(0)
        self.posExtOneTime = alternativeSummary.totTagFlows["Positive One-Time"] if "Positive One-Time" in alternativeSummary.totTagFlows else Decimal(0)
        self.negExtRecur = alternativeSummary.totTagFlows["Negative Recurring"] if "Negative Recurring" in alternativeSummary.totTagFlows else Decimal(0)
        self.negExtOneTime = alternativeSummary.totTagFlows["Negative One-Time"] if "Negative One-Time" in alternativeSummary.totTagFlows else Decimal(0)
        self.pvBens = alternativeSummary.totalBenefits
        self.pvCosts = alternativeSummary.totalCosts
        self.pvExts = pvExts
        self.respRec = alternativeSummary.totTagFlows["Response and Recovery"] if "Response and Recovery" in alternativeSummary.totTagFlows else Decimal(0)
        self.dirLossRed = alternativeSummary.totTagFlows["Direct Loss Reduction"] if "Direct Loss Reduction" in alternativeSummary.totTagFlows else Decimal(0)
        self.indirLossRed = alternativeSummary.totTagFlows["Indirect Loss Reduction"] if "Indirect Loss Reduction" in alternativeSummary.totTagFlows else Decimal(0)
        self.fatAvert = fatAvert
        self.valFatAvert = alternativeSummary.totTagFlows["Fatalities Averted"] if "Fatalities Averted" in alternativeSummary.totTagFlows else Decimal(0)
        self.ndrbRecur = alternativeSummary.totTagFlows["NDRB Recurring"] if "NDRB Recurring" in alternativeSummary.totTagFlows else Decimal(0)
        self.ndrbOneTime = alternativeSummary.totTagFlows["NDRB One-Time"] if "NDRB One-Time" in alternativeSummary.totTagFlows else Decimal(0)
        self.npvExts = alternativeSummary.netBenefits
        self.bcrExts = alternativeSummary.BCR
        self.irrExts = alternativeSummary.IRR
        self.roiExts = roiExts
        self.nonDisRoiExts = nonDisRoiExts
        self.npvNoExts = npvNoExts
        self.bcrNoExts = bcrNoExts
        self.irrNoExts = irrNoExts
        self.roiNoExts = roiNoExts
        self.nonDisRoiNoExts = nonDisRoiNoExts
        self.otherTags = filter_tags(alternativeSummary.totTagFlows, alternativeSummary.altID)

    # Allows for object to be directly printed out to console when testing, has no use in final code
    def __str__(self):
        print("altID:", self.altID)
        print("totalDirectCosts:", self.totalDirectCosts)
        print("totalIndirectCosts:", self.totalIndirectCosts)
        print("omrRecur:", self.omrRecur)
        print("omrOneTime:", self.omrOneTime)
        print("posExtRecur:", self.posExtRecur)
        print("posExtOneTime:", self.posExtOneTime)
        print("negExtRecur:", self.negExtRecur)
        print("negExtOneTime:", self.negExtOneTime)
        print("pvBens:", self.pvBens)
        print("pvCosts:", self.pvCosts)
        print("pvExts:", self.pvExts)
        print("respRec:", self.respRec)
        print("dirLossRed:", self.dirLossRed)
        print("indirLossRed:", self.indirLossRed)
        print("fatAvert:", self.fatAvert)
        print("valFatAvert:", self.valFatAvert)
        print("ndrbRecur:", self.ndrbRecur)
        print("ndrbOneTime:", self.ndrbOneTime)
        print("npvExts:", self.npvExts)
        print("bcrExts:", self.bcrExts)
        print("irrExts:", self.irrExts)
        print("roiExts:", self.roiExts)
        print("nonDisRoiExts:", self.nonDisRoiExts)
        print("npvNoExts:", self.npvNoExts)
        print("bcrNoExts:", self.bcrNoExts)
        print("irrNoExts:", self.irrNoExts)
        print("roiNoExts:", self.roiNoExts)
        print("nonDisRoiNoExts:", self.nonDisRoiNoExts)
        print("otherTags:", self.otherTags)
        return "--------------------End of Object--------------------"
