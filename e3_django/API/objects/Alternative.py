class Alternative:
    """
    Represents an alternative object in the API input.
    """

    def __init__(self, altID, altName, altBCNList, baselineBool):
        # Alternative ID
        self.altID = altID

        # Alternative Name
        self.altName = altName

        # List of BCN IDs included in this alternative
        self.altBCNList = altBCNList

        # True if this alternative is the baseline alternative, otherwise false
        self.baselineBool = baselineBool
