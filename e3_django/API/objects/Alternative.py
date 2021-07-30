class Alternative:
    """
    Represents an alternative object in the API input.
    """

    def __init__(self, altID, altName, altBCNList, baselineBool):
        self.altID = altID
        self.altName = altName
        self.altBCNList = altBCNList
        self.baselineBool = baselineBool
