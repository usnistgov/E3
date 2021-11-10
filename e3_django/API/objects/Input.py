from typing import Sequence, List

from API.objects import Alternative, Analysis, Bcn, Sensitivity


class Input:
    """
    Represents the full API input object.
    """

    def __init__(self, analysisObject: Analysis, alternativeObjects: List[Alternative], bcnObjects,
                 sensitivityObject=None, scenarioObject=None):
        # Object which defines general analysis parameters
        self.analysisObject = analysisObject

        # List of alternative objects
        self.alternativeObjects = alternativeObjects

        # List of BCN objects
        self.bcnObjects: Sequence[Bcn] = bcnObjects

        # Sensitivity object
        self.sensitivityObjects = sensitivityObject

        # Scenario object
        self.scenarioObject = scenarioObject
