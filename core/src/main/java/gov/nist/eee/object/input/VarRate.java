package gov.nist.eee.object.input;

public enum VarRate {
    /**
     * Denotes that the variability rate should compound year over year.
     */
    PERCENT_DELTA,

    /**
     * Denotes that the variability rate is for each individual year.
     */
    YEAR_BY_YEAR //Change name of year-by-year
}
