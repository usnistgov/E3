class EdgesSensitivitySummary():
    """
    Represents an edges summary object.
    """
    def __init__(self, globalVarBool, bcnObj, varName, diffType, diffVal, diffSign, edges_summaries):
        self.globalVarBool = globalVarBool
        self.bcnObj = bcnObj
        self.varName = varName
        self.diffType = diffType
        self.diffVal = diffVal
        self.diffSign = diffSign
        self.totalDirectCosts = {edges_summary.altID: edges_summary.totalDirectCosts for edges_summary in edges_summaries}
        self.totalIndirectCosts = {edges_summary.altID: edges_summary.totalIndirectCosts for edges_summary in edges_summaries}
        self.omrRecur = {edges_summary.altID: edges_summary.omrRecur for edges_summary in edges_summaries}
        self.omrOneTime = {edges_summary.altID: edges_summary.omrOneTime for edges_summary in edges_summaries}
        self.posExtRecur = {edges_summary.altID: edges_summary.posExtRecur for edges_summary in edges_summaries}
        self.posExtOneTime = {edges_summary.altID: edges_summary.posExtOneTime for edges_summary in edges_summaries}
        self.negExtRecur = {edges_summary.altID: edges_summary.negExtRecur for edges_summary in edges_summaries}
        self.negExtOneTime = {edges_summary.altID: edges_summary.negExtOneTime for edges_summary in edges_summaries}
        self.pvBens = {edges_summary.altID: edges_summary.pvBens for edges_summary in edges_summaries}
        self.pvCosts = {edges_summary.altID: edges_summary.pvCosts for edges_summary in edges_summaries}
        self.pvExts = {edges_summary.altID: edges_summary.pvExts for edges_summary in edges_summaries}
        self.respRec = {edges_summary.altID: edges_summary.respRec for edges_summary in edges_summaries}
        self.dirLossRed = {edges_summary.altID: edges_summary.dirLossRed for edges_summary in edges_summaries}
        self.indirLossRed = {edges_summary.altID: edges_summary.indirLossRed for edges_summary in edges_summaries}
        self.fatAvert = {edges_summary.altID: edges_summary.fatAvert for edges_summary in edges_summaries}
        self.valFatAvert = {edges_summary.altID: edges_summary.valFatAvert for edges_summary in edges_summaries}
        self.ndrbRecur = {edges_summary.altID: edges_summary.ndrbRecur for edges_summary in edges_summaries}
        self.ndrbOneTime = {edges_summary.altID: edges_summary.ndrbOneTime for edges_summary in edges_summaries}
        self.npvExts = {edges_summary.altID: edges_summary.npvExts for edges_summary in edges_summaries}
        self.bcrExts = {edges_summary.altID: edges_summary.bcrExts for edges_summary in edges_summaries}
        self.irrExts = {edges_summary.altID: edges_summary.irrExts for edges_summary in edges_summaries}
        self.roiExts = {edges_summary.altID: edges_summary.roiExts for edges_summary in edges_summaries}
        self.nonDisRoiExts = {edges_summary.altID: edges_summary.nonDisRoiExts for edges_summary in edges_summaries}
        self.npvNoExts = {edges_summary.altID: edges_summary.npvNoExts for edges_summary in edges_summaries}
        self.bcrNoExts = {edges_summary.altID: edges_summary.bcrNoExts for edges_summary in edges_summaries}
        self.irrNoExts = {edges_summary.altID: edges_summary.irrNoExts for edges_summary in edges_summaries}
        self.roiNoExts = {edges_summary.altID: edges_summary.roiNoExts for edges_summary in edges_summaries}
        self.nonDisRoiNoExts = {edges_summary.altID: edges_summary.nonDisRoiExts for edges_summary in edges_summaries}
        self.otherTags = {edges_summary.altID: edges_summary.otherTags for edges_summary in edges_summaries}

    # Allows for object to be directly printed out to console when testing, has no use in final code
    def __str__(self):
        print("globalVarBool:", self.globalVarBool)
        print("bcnObj:", self.bcnObj)
        print("varName:", self.varName)
        print("diffType:", self.diffType)
        print("diffVal:", self.diffVal)
        print("diffSign:", self.diffSign)
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
