from typing import Union

from celery import shared_task

from API import registry
from API.libraries import cashFlow
from API.objects.Input import Input


@shared_task
def analyze(user_input: Input):
    """
    Main task that runs analysis.

    :param user_input: The input object the user provides.
    :return: The json output created by the analysis.
    """

    analysis = user_input.analysisObject

    # Loop through all bcn instances and generate all associated bcnStorage objects. The loop structure should work
    # within django, if not we may need to move to a registry metaclass. The first call generates the cash and
    # quantity flows for the bcn, the second generates the bcnStorage object for the associated bcn. Considering this
    # process is repeated for the sensitivity # and uncertainty calculations the following steps will eventually be
    # moved to a separate function or possibly their own script if they take up a significant portion of the code;
    # calculating and generating bcnStorage objects, # calculating and generating total flows, calculating and
    # generating measures, converting output to json format for passing user data back
    discountRate = analysis.dRateReal
    studyPeriod = analysis.studyPeriod
    timestepCount = analysis.timestepComp
    timestepValue = analysis.timestepVal

    for bcn in user_input.bcnObjects:
        bcnNonDiscFlow, bcnDiscFlow, quantList = cashFlow.bcnFlow(discountRate, bcn, studyPeriod, timestepCount)

    # Generate the total flows for each alternative. First the list of all altIDs is generated. This is done by
    # looping through the alternative registry (or a metaclass can be used). The code then loops through the
    # bcnStorage registry to sum all items related to a particular alternative. From there the code generates the
    # totalRequiredFlows and totalOptionalFlows objects for each alternative via the call to cashFlows. altIDList
    # will be used often.
    for alt in user_input.alternativeObjects:
        if alt.baselineBoolean:
            baselineID = alt.altID
        cashFlow.totalFlows(alt.altID, studyPeriod, timestepValue, alt.baselineBoolean, bcnStorage.objects.all())

    # Create baseline measures
    baselineAlt = [totRFlow for totRFlow in totalRequiredFlows._registry if totRFlow.altID == baselineID]
    baselineFlowList, baselineMeasList = measures.calcBaselineMeas(baselineAlt)

    # Create baseline tag measures
    baslineTagList = []
    for totOptFlow in totalOptionalFlows.objects.all():
        measures.calcBaslineTagMeas(baselineTagList, baselineAlt, totOptFlow.altID, totOptFlow.tag,
                                    totOptFlow.totalTagFlowDisc, totOptFlow.totTagQ, totOptFlow.quantUnits)

    # Create baseline quantitiy attributes
    baselineQSum, baselineQUnits = quantList(baselineTagList)

    # Construct Baseline alternative Summary Object
    alternativeSummary(*baselineMeasList, baselineQSum, baselineQUnits, analysis.marr, None, None, None, None)

    # Calculate alternative measures
    for totRFlow in totalRequiredFlows.objects.all():
        if totRFlow != baselineID:
            altID = totRFlow.altID
            altMeasList = calcAltMeas(altID, baselineFlowList, reinvestRate, totRFlow)

            altTagList = []
            quantMeasList = []
            deltaQuant = []
            nsDeltaQuant = []
            nsPercQuant = []
            nsElasticityQuant = []
            for totOptFlow in totalOptionalFlows.objects.all():
                if altID == totOptFlow.altID:
                    altTagMeasList = calcAltTagMeas(altMeasList, baselineTagList, totOptFlow.tag,
                                                    totOptFlow.totalTagFlowDisc,
                                                    totOptFlow.totTagQ, totOptFlow.quantUnits)

            altQSum, altQUnits = quantList(altTagList)

            alternativeSummary(*altMeasList, altQSum, altQUnits, analysis.marr, *altTagMeasList)

    return []


@shared_task
def runModule(outputOption: Union[str, list[str]], userInput):
    return registry.moduleFunctions[outputOption](userInput)
