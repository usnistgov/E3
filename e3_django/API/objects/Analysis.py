class Analysis:
    def __init__(
            self,
            analysisType,
            objToReport,
            studyPeriod,
            baseDate,
            timestepVal,
            timestepComp,
            Marr,
            noAlt,
            baseAlt,
            reinvestRate,
            projectType=None,
            serviceDate=None,
            outputRealBool=None,
            interestRate=None,
            dRateReal=None,
            dRateNom=None,
            inflationRate=None,
            incomeRateFed=None,
            incomeRateOther=None,
            location=None,
    ):
        self.analysisType = analysisType
        self.objToReport = objToReport
        self.studyPeriod = studyPeriod
        self.baseDate = baseDate
        self.timestepVal = timestepVal
        self.timestepComp = timestepComp
        self.Marr = Marr
        self.noAlt = noAlt
        self.baseAlt = baseAlt
        self.reinvestRate = reinvestRate
        self.projectType = projectType
        self.serviceDate = serviceDate
        self.outputRealBool = outputRealBool
        self.interestRate = interestRate
        self.dRateReal = dRateReal
        self.dRateNom = dRateNom
        self.inflationRate = inflationRate
        self.incomeRateFed = incomeRateFed
        self.incomeRateOther = incomeRateOther
        self.location = location