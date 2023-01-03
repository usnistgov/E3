import math
import operator
import numpy
from decimal import Decimal
from typing import Iterable

from API.registry import E3ModuleConfig
from rest_framework.fields import ListField
from compute.serializers import EdgesSummarySerializer
from compute.objects import RequiredCashFlow, OptionalCashFlow, EdgesSummary, AlternativeSummary, SensitivitySummary
from compute.objects.AlternativeSummary import bcr, irrMeas
from API.objects import Analysis, Alternative


class EdgesConfig(E3ModuleConfig):
    """
    This module updates BCNs and Sensitivity objects for disaster related benefits.
    """

    name = "compute.edges"
    verbose_name = 'E3 EDGeS Calculations'
    depends_on = ["FlowSummary", "OptionalSummary", "MeasureSummary", "internal:cash-flows"]
    output = "EdgesSummary"
    serializer = ListField(child=EdgesSummarySerializer(), required=False)

    def run(self, base_input, dependencies=None):
        horizon = base_input.analysisObject.studyPeriod
        for alt in base_input.alternativeObjects:
            if alt.baselineBool is True:
                baseline_id = alt.altID

        return calculate_edges_summary(horizon, baseline_id, base_input.alternativeObjects,
                                       dependencies["FlowSummary"], dependencies["OptionalSummary"],
                                       dependencies["MeasureSummary"])


def elementwise_subtract(x, y):
    return list(map(operator.sub, x, y))


def calculate_edges_summary(horizon, baseline_id, alternatives: Iterable[Alternative],
                            required_flows: Iterable[RequiredCashFlow], optional_flows: Iterable[OptionalCashFlow],
                            alternative_summaries: Iterable[AlternativeSummary],
                            sensitivity_summaries: Iterable[SensitivitySummary] = None):

    # Variable definitions, "nb" - net benefits, "wd" or "d" - with disaster, "wod" - without disaster, "we" - with
    # externalities, "woe" - without externalities, "drb" - disaster related benefits

    # 1. Find baseline and reorder list so that it is first in list. Prevents re-looping in order for calculations to
    # run properly
    alt_list = [0]
    res = []
    for alt in alternatives:
        if alt.altID == baseline_id:
            alt_list[0] = alt
        else:
            alt_list.append(alt)

    # 2. Collect cash flows from base E3 analysis needed to calculate additional measures for Edges Output
    for alt in alt_list:
        # 2.1. Collect values from required flows
        for req_flow in required_flows:
            if alt.altID == baseline_id:
                baseline_cost_non_disc = req_flow.totCostNonDisc
                baseline_bens_non_disc = req_flow.totBenefitsNonDisc
                # DRB flows may not be externalities at present
                baseline_ext_disc = elementwise_subtract(req_flow.totBenefitsExtDisc, req_flow.totCostExtDisc)
                baseline_ext_non_disc = elementwise_subtract(req_flow.totBenefitsExt, req_flow.totCostExt)
            elif alt.altID == req_flow.altID:
                tot_cost_non_disc = req_flow.totCostNonDisc
                tot_bens_non_disc = req_flow.totBenefitsNonDisc
                # DRB flows may not be externalities at present
                tot_ext_disc = elementwise_subtract(req_flow.totBenefitsExtDisc, req_flow.totCostExtDisc)
                tot_ext_non_disc = elementwise_subtract(req_flow.totBenefitsExt, req_flow.totCostExt)

        # 2.2. Collect values from optional flows
        for opt_flow in optional_flows:
            if opt_flow.altID == alt.altID and (opt_flow.tag == "DRB" or opt_flow.tag == "DRB-Ext"):
                if alt.altID == baseline_id:
                    base_drb_flow_non_disc = opt_flow.totTagFlowNonDisc
                else:
                    drb_flow_non_disc = opt_flow.totTagFlowNonDisc
            if opt_flow.altID == alt.altID and opt_flow.tag == "Fatalities Averted":
                if alt.altID == baseline_id:
                    base_fat_avert = Decimal(numpy.sum(opt_flow.totTagQ))
                else:
                    fat_avert = Decimal(numpy.sum(opt_flow.totTagQ))
        try:
            fat_avert
        except UnboundLocalError:
            fat_avert = Decimal(0)
        # try:
        #     base_fat_avert
        # except UnboundLocalError:
        #     base_fat_avert = Decimal(0)
        #
        # fat_avert_diff = fat_avert - base_fat_avert

            # The following code is used if we want to allow DRB related externalities, currently has no impact on
            # calculations. This is mainly here as a reminder. If implemented the tag should be "DRB" and an additional
            # check should be made against the corresponding BCN's subtype (would need to remove "DRB-Ext" check from
            # previous conditional as well as here).
            # if opt_flow.altID == alt.altID and opt_flow.tag == "DRB-Ext":
            #     if alt.altID == baseline_id:
            #         base_drb_ext_flow_non_disc = opt_flow.totTagFlowNonDisc
            #     else:
            #         drb_ext_flow_non_disc = opt_flow.totTagFlowNonDisc

        # 3. Pull useful values from the appropriate AlternativeSummary objects
        for alt_summ in alternative_summaries:
            # 3.1. Pull values used to calculate new output
            if alt.altID == baseline_id:
                try:
                    base_npv_d_disc = alt_summ.totTagFlows["DRB"]
                except KeyError:
                    base_npv_d_disc = 0
                base_npv_inv_costs = alt_summ.totalCostsInv
                base_npv_benefits = alt_summ.totalBenefits
                base_npv_non_inv_costs = alt_summ.totalCostsNonInv
                baseline_ext = numpy.sum(baseline_ext_disc)
                break
            if alt.altID == alt_summ.altID and alt.altID != baseline_id:
                nb_wd_we_disc = alt_summ.netBenefits
                try:
                    npv_d_disc = alt_summ.totTagFlows["DRB"]
                except KeyError:
                    npv_d_disc = 0
                npv_inv_costs = alt_summ.totalCostsInv
                npv_benefits = alt_summ.totalBenefits
                npv_non_inv_costs = alt_summ.totalCostsNonInv
                break

            total_costs = alt_summ.totalCosts

        # 4. Calculate new outputs for EDGe$ analysis
        if alt.altID != baseline_id:
            total_ext = numpy.sum(tot_ext_disc)
            nb_wd_woe_disc = nb_wd_we_disc - (total_ext - baseline_ext)
            nb_wod_woe_disc = nb_wd_woe_disc - (total_ext - baseline_ext) - (npv_d_disc - base_npv_d_disc)
            nb_wod_we_disc = nb_wd_we_disc - (npv_d_disc - base_npv_d_disc)
        else:
            total_ext = numpy.sum(baseline_ext_disc)
            nb_wd_woe_disc = None
            nb_wod_woe_disc = None
            nb_wod_we_disc = None

        if alt.altID != baseline_id:
            roi_wd_we = annualized_roi(nb_wd_we_disc, npv_inv_costs - base_npv_inv_costs, horizon)
            roi_wd_woe = annualized_roi(nb_wd_woe_disc, npv_inv_costs - base_npv_inv_costs, horizon)
            roi_wod_we = annualized_roi(nb_wod_we_disc, npv_inv_costs - base_npv_inv_costs, horizon)
            roi_wod_woe = annualized_roi(nb_wod_woe_disc, npv_inv_costs - base_npv_inv_costs, horizon)

            bcr_wd_woe = bcr(npv_benefits - total_ext, base_npv_benefits - baseline_ext, npv_inv_costs,
                             base_npv_inv_costs, npv_non_inv_costs, base_npv_non_inv_costs)
            # bcr_wod_we = bcr(npv_benefits - npv_d_disc, base_npv_benefits - base_npv_d_disc, npv_inv_costs,
            #                 base_npv_inv_costs, npv_non_inv_costs, base_npv_non_inv_costs)
            # bcr_wod_woe = bcr(npv_benefits - total_ext - npv_d_disc, base_npv_benefits - baseline_ext - base_npv_d_disc,
            #                  npv_inv_costs, base_npv_inv_costs, npv_non_inv_costs, base_npv_non_inv_costs)

            diff1 = elementwise_subtract(tot_bens_non_disc, tot_ext_non_disc)
            base_diff1 = elementwise_subtract(baseline_bens_non_disc, baseline_ext_non_disc)
            # diff2 = elementwise_subtract(tot_bens_non_disc, drb_flow_non_disc)
            # base_diff2 = elementwise_subtract(baseline_bens_non_disc, base_drb_flow_non_disc)
            # diff3 = elementwise_subtract(diff1, drb_flow_non_disc)
            # base_diff3 = elementwise_subtract(base_diff1, base_drb_flow_non_disc)

            irr_wd_woe = irrMeas(tot_cost_non_disc, diff1, baseline_cost_non_disc, base_diff1, "Continuous")
            # irr_wod_we = irrMeas(tot_cost_non_disc, diff2, baseline_cost_non_disc, base_diff2, "Continuous")
            # irr_wod_woe = irrMeas(tot_cost_non_disc, diff3, baseline_cost_non_disc, base_diff3, "Continuous")
        else:
            roi_wd_we = None
            roi_wd_woe = None
            roi_wod_we = None
            roi_wod_woe = None

            bcr_wd_woe = None
            # bcr_wod_we = None
            # bcr_wod_woe = None

            irr_wd_woe = None
            # irr_wod_we = None
            # irr_wod_woe = None

        # 5. Construct Edges output objects
        res.append(EdgesSummary(alt.altID, alt_summ, total_ext, fat_avert, roi_wd_we, roi_wod_we, nb_wd_woe_disc,
                                bcr_wd_woe, irr_wd_woe, roi_wd_woe, roi_wod_woe))
    return res
    # 6. Repeat for Sensitivity calculations (make functions to clean up repeated calculations)
    # Check if sensitivity objects exist
    # Loop through BCNs, look for externalities and DRB tagged variables
    # Use calls to cash_flows(bcn, analysis.studyPeriod, discount_rate, timestep_comp) to generate the dictionary
    # needed to sum necessary flows for calculations w/o DRBs and w/o Externalities
    # Option 2: break into multiple alternatives in the input override section of code in task.py. May not work
    # for uncertainty


def annualized_roi(net_benefit, inv_cost, horizon):
    # Calculate ROI (Move to measures if this is going to be used by more than just Edges)
    try:
        return (net_benefit/inv_cost) * 100 * 1/Decimal(horizon)
    except ZeroDivisionError:
        return None
