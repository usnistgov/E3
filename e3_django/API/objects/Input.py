from typing import Sequence

from API.objects import Alternative, Analysis, Bcn


class Input:
    def __init__(self, analysisObject: Analysis, alternativeObjects: list[Alternative], bcnObjects, sensitivityObject=None,
                 scenarioObject=None):
        self.analysisObject = analysisObject
        self.alternativeObjects = alternativeObjects
        self.bcnObjects: Sequence[Bcn] = bcnObjects
        self.sensitivityObject = sensitivityObject
        self.scenarioObject = scenarioObject
