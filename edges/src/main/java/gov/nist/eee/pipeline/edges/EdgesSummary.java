package gov.nist.eee.pipeline.edges;

import java.util.List;
import java.util.Map;

public record EdgesSummary(
        double totalDirectCosts,
        double totalIndirectCosts,
        double omrRecur,
        double omrOneTime,
        double posExtRecur,
        double posExtOneTime,
        double negExtRecur,
        double negExtOneTime,
        double pvBens,
        double pvCosts,
        double pvExts,
        double respRec,
        double dirLossRed,
        double indirLossRed,
        double fatAvert,
        double valFatAvert,
        double ndrbRecur,
        double ndrbOneTime,
        double npvExts,
        double bcrExts,
        double irrExts,
        double roiExts,
        double nonDisRoiExts,
        double npvNoExts,
        double bcrNoExts,
        double irrNoExts,
        double roiNoExts,
        double nonDisRoiNoExts,
        Map<String, Double> otherTags
) {
}
