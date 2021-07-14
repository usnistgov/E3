from API.objects.Analysis import Analysis


class Input:
    def __init__(self, analysisObject: Analysis, alternativeObjects, bcnObjects, sensitivityObject=None,
                 scenarioObject=None):
        self.analysisObject = analysisObject
        self.alternativeObjects = alternativeObjects
        self.bcnObjects = bcnObjects
        self.sensitivityObject = sensitivityObject
        self.scenarioObject = scenarioObject
