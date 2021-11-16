def calculate_inflation_rate(discount_rate_nom, discount_rate_real):
    """
    Returns inflation rate from nominal and real discount rates if user fails to provide an inflation rate.
    """
    return (1 + discount_rate_nom) / (1 + discount_rate_real) - 1


def calculate_discount_rate_nominal(inflation_rate, discount_rate_real):
    """
    Returns the nominal discount rate from inflation and real discount rates if user fails to provide a nominal
    discount rate.
    """
    if not inflation_rate or not discount_rate_real:
        raise(Exception("Both real discount rate and inflation rate must be provided."))
    return (1 + inflation_rate) * (1 + discount_rate_real) - 1


def calculate_discount_rate_real(discount_rate_nom, inflation_rate):
    """
    Returns the real discount rate from inflation and nominal discount rates if user fails to provide real
    discount rate.
    """
    if not discount_rate_nom or not inflation_rate:
        raise(Exception("Both nominal discount rate and inflation rate must be provided."))
    return (1 + discount_rate_nom) / (1 + inflation_rate) - 1


class Analysis:
    """
    Represents the analysis options object of the API input.
    """

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
        # Type of this analysis request.
        self.analysisType = analysisType

        # List of output objects to calculate as strings.
        self.objToReport = objToReport

        # Length of study period.
        self.studyPeriod = studyPeriod

        # Base date for this analysis. (Unused)
        self.baseDate = baseDate

        # Type of timestep, e.g. "Year", "month", etc.
        self.timestepVal = timestepVal

        # Number of timestep types between each time period.
        self.timestepComp = timestepComp

        # MARR.
        self.Marr = Marr

        # Number of alternatives.
        self.noAlt = noAlt

        # ID of baseline alternative.
        self.baseAlt = baseAlt

        # Reinvestment rate.
        self.reinvestRate = reinvestRate

        # Project Type.
        self.projectType = projectType

        # Service Date.
        self.serviceDate = serviceDate

        # True if the output should be real or false if output should be nominal.
        self.outputRealBool = outputRealBool

        # Interest Rate.
        self.interestRate = interestRate

        # Real discount rate.
        self.dRateReal = dRateReal

        # Nominal discount rate.
        self.dRateNom = dRateNom

        # Inflation Rate.
        self.inflationRate = inflationRate

        # Federal income rate tax.
        self.incomeRateFed = incomeRateFed

        # Other income rate tax.
        self.incomeRateOther = incomeRateOther

        # Location of analysis given as list of strings, e.g. ["United States", "Maryland", "20879"]
        self.location = location


        # If outputRealBool is false, all three values should have been provided/calculated.
        if not self.outputRealBool:
            if not (self.inflationRate and self.dRateReal and dRateNom): 
                # Single missing value should have been calculated in AnalysisSerializer.
                raise AssertionError("Cannot calculate one of inflation rate, discount rate real or discount rate nominal.")
        # If outputRealBool is true, real discount rate must have been provided/calculated.
        else: 
            if not self.dRateReal:
                # If real discount rate was not provided by user, should have been calculated in AnalysisSerializer.
                raise AssertionError("Cannot calculate discount real rate.")
