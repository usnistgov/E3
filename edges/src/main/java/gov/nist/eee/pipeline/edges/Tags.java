package gov.nist.eee.pipeline.edges;

import java.util.List;

public class Tags {
    public static final String DRB = "DRB";
    public static final String DRB_EXTERNAL = "DRB-Ext";
    public static final String OMR_RECURRING = "OMR Recurring";
    public static final String OMR_ONE_TIME = "OMR One-Time";
    public static final String POSITIVE_RECURRING = "Positive Recurring";
    public static final String POSITIVE_ONE_TIME = "Positive One-Time";
    public static final String NEGATIVE_RECURRING = "Negative Recurring";
    public static final String NEGATIVE_ONE_TIME = "Negative One-Time";
    public static final String RESPONSE_AND_RECOVERY = "Response and Recovery";
    public static final String DIRECT_LOSS_REDUCTION = "Direct Loss Reduction";
    public static final String INDIRECT_LOSS_REDUCTION = "Indirect Loss Reduction";
    public static final String FATALITIES_AVERTED = "Fatalities Averted";
    public static final String NDRB_RECURRING = "NDRB Recurring";
    public static final String NDRB_ONE_TIME = "NDRB One-Time";
    public static final List<String> EDGES_TAGS = List.of(
            OMR_RECURRING, OMR_ONE_TIME, POSITIVE_RECURRING, POSITIVE_ONE_TIME, NEGATIVE_RECURRING, NEGATIVE_ONE_TIME,
            RESPONSE_AND_RECOVERY, DIRECT_LOSS_REDUCTION, INDIRECT_LOSS_REDUCTION, FATALITIES_AVERTED,
            NDRB_RECURRING, NDRB_ONE_TIME
    );
}
