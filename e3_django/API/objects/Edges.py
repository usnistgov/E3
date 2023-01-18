import logging
from copy import deepcopy
import math
from decimal import Decimal
from rest_framework.exceptions import ValidationError

logger = logging.getLogger(__name__)


def drb_future_value(value, disaster_rate, discount_rate, horizon, initial_occurrence):
    """
    Finds the future value of a disaster related benefit

    :param value: The monetary value of the DRB
    :param disaster_rate: The mean recurrence interval of the disaster
    :param discount_rate: The discount rate used in the analysis
    :param horizon: The planning horizon of the analysis
    :param initial_occurrence: The first occurrence of the DRB+
    :return: Future value of the DRB
    """
    # Define the lambda parameter for disaster recurrence
    lambda_param = 1 / disaster_rate

    # Calculate the future value numerator and denominator
    fv_numerator = math.exp(-(discount_rate + lambda_param) * horizon) - math.exp(-(discount_rate + lambda_param) *
                                                                                  initial_occurrence)
    fv_denominator = math.exp(-(discount_rate + lambda_param) * initial_occurrence) - \
                     math.exp(-(discount_rate + lambda_param) * horizon) - \
                     (discount_rate + lambda_param) / lambda_param

    # Return the future value of the disaster related event
    return value * Decimal(fv_numerator) / Decimal(fv_denominator)


def drb_annualized(future_value, discount_rate, horizon, initial_occurrence):
    """
    Uses the future value of the DRB to generate an annualized value

    :param future_value: The future value of the DRB (calculated in drb_future_value())
    :param discount_rate: The discount rate used in the analysis
    :param horizon: The planning horizon of the analysis
    :param initial_occurrence: The first occurrence of the DRB
    :return: Annualized DRB value
    """
    # Calculate the numerator and denominator required to get the annualized value from the future value
    av_denom_1 = (math.exp(-discount_rate * (initial_occurrence - 1)) - math.exp(-discount_rate * horizon))
    av_denom_2 = 1 / (math.exp(discount_rate) - 1)

    # Return the annualized value
    return future_value * 1 / (Decimal(av_denom_1) * Decimal(av_denom_2))


def sens_adjustment(sens_object, bcn_object, original_values, disaster_rate, discount_rate, horizon,
                    initial_occurrence):
    """
    The calculations required to adjust the sensitivity inputs to account for the probabilistic nature of DRBs

    :param sens_object: The sensitivity object being examined
    :param bcn_object: The bcn object related to the sensitivity object
    :param original_values: The original values from the BCN (i.e. before adjustment occurs)
    :param disaster_rate: The mean recurrence interval of the disaster
    :param discount_rate: The discount rate used in the analysis
    :param horizon: The planning horizon of the analysis
    :param initial_occurrence: The first occurrence of the DRB
    :return: Sensitivity object updated for DRBs
    """
    # Update the value based on the type of change
    if sens_object.varName == "valuePerQ":
        new_value = original_values[1] * (original_values[2] + sens_object.diffValue)
    else:
        new_value = (original_values[1] + sens_object.diffValue) * original_values[2]

    # Determine the future value of the base analysis and the value when the sensitivity alterations are applied
    base_future_value = drb_future_value(original_values[1] * original_values[2], disaster_rate, discount_rate,
                                         horizon, initial_occurrence)
    sens_future_value = drb_future_value(new_value, disaster_rate, discount_rate, horizon, initial_occurrence)

    # Find the difference between the future values
    diff_value = sens_future_value - base_future_value

    # Obtain the annualized value of the difference and update the sensitivity object with the new value
    if sens_object.varName == "valuePerQ":
        sens_object.diffValue = drb_annualized(diff_value, discount_rate, horizon, initial_occurrence) / \
                                bcn_object.quant
    else:
        sens_object.diffValue = drb_annualized(diff_value, discount_rate, horizon, initial_occurrence) / \
                                bcn_object.valuePerQ

    return None


class Edges:
    """
    Represents the sensitivity object of the API input.
    """
    def __init__(
        self,
        mri,
        drbList,
        # fatList,
        disMag,
        vosl,
        riskPref,
        confInt
    ):
        # Mean Recurrence Interval
        self.mri = mri
        # List of Disaster Related Benefits BCNs
        self.drbList = drbList
        # List of Fatality Related BCNs
        # self.fatList = fatList
        # Disaster Magnitude
        self.disMag = disMag
        # Value of a statistical life
        self.vosl = vosl
        # Risk Preference
        self.riskPref = riskPref
        # Value of Confidence Interval
        self.confInt = confInt

    def override_input(self, base_input):
        """
        Overrides user input to make DRB values suitable for use in E3. If EDGe$ eventually uses E3 this code should
        be moved to the front end.

        :param base_input: User input data
        :return:
        """
        # edges = base_input.edgesObject

        # 1. Collect necessary values
        disaster_rate = self.mri
        bcn_list = base_input.bcnObjects
        discount_rate = base_input.analysisObject.dRateReal if base_input.analysisObject.outputRealBool else base_input.analysisObject.dRateNom
        horizon = base_input.analysisObject.studyPeriod

        # 2. Initialize list to store unaltered values
        original_values = []

        # 3. Loop through bcns and the drb list to find bcns that need to be adjusted
        for bcn in bcn_list:
            for drb_id in self.drbList:
                if drb_id == bcn.bcnID:
                    # 3.1. Get original object values (not references to object variables) and store them
                    bcn_id = getattr(bcn, "bcnID")
                    quant = getattr(bcn, "quant")
                    value_per_q = getattr(bcn, "valuePerQ")
                    original_values.append([bcn_id, quant, value_per_q])
                    # 3.2. Calculate original non-discounted value and original future value for the bcn
                    value = bcn.valuePerQ*bcn.quant
                    future_value = drb_future_value(value, disaster_rate, discount_rate, horizon, bcn.initialOcc)
                    # 3.3. Calculate expected fatalities averted if appropriate
                    if "Fatalities Averted" in bcn.bcnTag:
                        bcn.quant = 1/disaster_rate*bcn.quant
                    # 3.4. Calculate annualized value and define valuePerQ. We assume that quant is 1.0 for all drbs
                    # excluding the fatalities averted.
                    bcn.valuePerQ = drb_annualized(future_value, discount_rate, horizon, bcn.initialOcc)/bcn.quant
                    # 3.5. Set remaining values to those required to ensure runs are proper
                    bcn.recurBool = True
                    # bcn.initialOcc = horizon
                    bcn.recurInterval = 1
                    bcn.recurEndDate = horizon
                    # Note: These values need not be None if the change is percentage based. Making this work for gross
                    # changes per year is feasible, but would require more code. Right now I'm only trying to copy
                    # Edges capabilities so all escalations are set to None since that's not supported in Edges. This
                    # should be caught in the validation. The definitions are remaining here in the event we want to do
                    # something with them in the future.
                    bcn.quantVarRate = None
                    bcn.quantVarValue = [0 for _ in range(horizon + 1)]
                    bcn.recurVarRate = None
                    bcn.recurVarValue = [0 for _ in range(horizon + 1)]

        # 4. Loop through Sensitivity Input objects, check against input list to see if BCN is a DRB. If true, calculate
        # the adjusted values for the sensitivity object (Formulas should work for uncertainty as well)
        if "EdgesSensitivitySummary" in base_input.analysisObject.objToReport:
            for sens_object in base_input.sensitivityObjects:
                bcn_id = sens_object.bcnID
                if sens_object.diffType == "Gross":
                    for bcn in bcn_list:
                        if bcn.bcnID == bcn_id:
                            bcn_object = bcn
                            break
                    for item in original_values:
                        if item[0] == bcn_id:
                            bcn_values = item
                            break
                    for drb_id in self.drbList:
                        if drb_id == bcn_id:
                            sens_adjustment(sens_object, bcn_object, bcn_values, disaster_rate, discount_rate, horizon,
                                            bcn_object.initialOcc)
                            break

        return None
