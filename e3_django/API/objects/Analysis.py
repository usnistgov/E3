
def inflationRateCalc(discount_rate_nom, discount_rate_real):
    """
    Purpose: Returns inflation rate from nominal and real discount rates,
    if user fails to provide an inflation rate.
    """
    return (1 + discount_rate_nom) / (1 + discount_rate_real) - 1


def dRateNomCalc(inflation_rate, discount_rate_real):
    """
    Purpose: Returns the nominal discount rate from inflation and real discount rates,
    if user fails to provide a nominal discount rate.
    """
    return (1 + inflation_rate) * (1 + discount_rate_real) - 1


def dRateRealCalc(discount_rate_norm, inflation_rate):
    """
    Purpose: Returns the real discount rate from inflation and nominal discount rates,
    if user fails to provide real discount rate.
    """
    return (1 + discount_rate_norm) / (1 + inflation_rate) - 1


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

        if not (self.inflationRate and self.dRateReal and dRateNom):
            if self.inflationRate is None and self.dRateReal and self.dRateNom:
                self.inflationRate = inflationRateCalc(self.dRateNom, self.dRateReal)
            elif self.dRateReal is None and self.inflationRate and self.dRateNom:
                self.dRateReal = dRateRealCalc(self.dRateNom, self.inflationRate)
            elif self.dRateNom is None and self.inflationRate and self.dRateReal:
                self.dRateNom = dRateNomCalc(self.inflationRate, self.dRateReal)
            else:
                raise AssertionError("Cannot calculate one of inflation rate, discount rate real or discount rate "
                                     "nominal")
