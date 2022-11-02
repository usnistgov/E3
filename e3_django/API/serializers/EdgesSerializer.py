from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError
from rest_framework.fields import IntegerField, ChoiceField, ListField

from API.serializers.fields import InfinityDecimalField
from API.variables import MAX_DIGITS, DECIMAL_PLACES, NUM_ERRORS_LIMIT
import logging

logger = logging.getLogger(__name__)


class EdgesSerializer(Serializer):
    mri = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=True)
    drbList = ListField(child=IntegerField(), required=True, allow_null=True)
    disMag = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)
    riskPref = ChoiceField(["Averse", "Neutral", "Accepting"], required=False)
    confInt = InfinityDecimalField(max_digits=MAX_DIGITS, decimal_places=DECIMAL_PLACES, required=False)

    def validate(self, data):
        errors = []
        study_period = data["analysisObject"]["studyPeriod"]

        if not data["mri"] or data["mri"] <= 0:
            errors.append(
                ValidationError(
                    "MRI must be a positive numeric value."
                )
            )

        if not data["drbList"]:
            errors.append(
                ValidationError(
                    "There must be at least one disaster related benefit for an EDGe$ analysis to be performed."
                )
            )

        if data["analysisObject"]["comp_type"] != "Continuous":
            errors.append(
                ValidationError(
                    "Compounding type must be continuous."
                )
            )

        alt_list = []
        for x in data["alternativeObjects"]:
            alt_list += x["altBCNList"]

        for bcnID in data["drbList"]:
            if bcnID not in alt_list:
                errors.append(
                    ValidationError(
                        "The BCN selected as a disaster related benefit must correspond to an existing BCN object."
                    )
                )

        # Remove pertinent sections if we allow DRB related Externalities or other bcn definitions not currently allowed
        # in Edges (i.e. Disaster related costs, escalation of DRBs, etc.)
        bcn_list = data["bcnObjects"]
        for bcn in bcn_list:
            if "DRB" in bcn["bcnTag"]:
                if bcn["subType"] == "Externality":
                    errors.append(
                        ValidationError(
                            "Disaster Related Benefits may not be treated as Externalities in the analysis."
                        )
                    )
                if bcn["subType"] == "Cost":
                    errors.append(
                        ValidationError(
                            "Disaster Related Benefits may not be treated as Costs in the analysis."
                        )
                    )
                if bcn["bcnInvestBool"] is True:
                    errors.append(
                        ValidationError(
                            "Disaster Related Benefits may not be treated as Investment Costs in the analysis."
                        )
                    )
                if bcn["recurVarRate"]:
                    errors.append(
                        ValidationError(
                            "Disaster Related Benefits may not have escalating values in the analysis."
                        )
                    )
                if bcn["quantVarRate"]:
                    errors.append(
                        ValidationError(
                            "Disaster Related Benefits may not have escalating quantities in the analysis."
                        )
                    )
                try:
                    if float(bcn["recurInterval"]) != 1:
                        errors.append(
                            ValidationError(
                                "Disaster Related Benefits must be recurring with an interval of 1."
                            )
                        )
                except ValueError:
                    errors.append(
                        ValidationError(
                            "Disaster Related Benefits must be recurring with an interval of 1."
                        )
                    )
                if bcn["recurBool"] is False:
                    errors.append(
                        ValidationError(
                            "Disaster Related Benefits must be recurring with an interval of 1."
                        )
                    )
                if bcn["EndDate"] not in [study_period, None]:
                    errors.append(
                        ValidationError(
                            "Disaster Related Benefits cannot terminate before the end of the study period."
                        )
                    )
                if "Response and Recovery" not in bcn["bcnTag"] or "Direct Loss Reduction" not in bcn["bcnTag"] \
                        or "Indirect Loss Reduction" not in bcn["bcnTag"] or "Fatalities Averted" not in bcn["bcnTag"]:
                    errors.append(
                        ValidationError(
                            "DRBs must be tagged as \"Response and Recovery\", \"Direct Loss Reduction\", \"Indirect Loss Reduction\" or \"Fatalities Averted\" for output purposes"
                        )
                    )
                    # End remove block
            if bcn["bcnSubType"] == "Externality" and ("Positive One-Time" not in bcn["bcnTag"]
                                                       or "Positive Recurring" not in bcn["bcnTag"]
                                                       or "Negative One-Time" not in bcn["bcnTag"]
                                                       or "Negative Recurring" not in bcn["bcnTag"]):
                errors.append(
                    ValidationError(
                        "Externalities must be tagged as \"Positive One-time\", \"Positive Recurring\", \"Negative One-time\" or \"Negative Recurring\" for output purposes"
                    )
                )
            if bcn["bcnType"] == "Cost" and "OMR" in bcn["bcnTag"] and ("OMR One-Time" not in bcn["bcnTag"]
                                                                        or "OMR Recurring" not in bcn["bcnTag"]):
                errors.append(
                    ValidationError(
                        "OMR costs must be tagged as \"OMR One-Time\" or \"OMR Recurring\" for output purposes"
                    )
                )
            if bcn["bcnType"] != "Cost" and "OMR" in bcn["bcnTag"] or "OMR One-Time" in bcn["bcnTag"] \
                    or "OMR Recurring" in bcn["bcnTag"]:
                errors.append(
                    ValidationError(
                        "OMR must be a Cost type BCN"
                    )
                )
            if "NDRB" in bcn["bcnTag"] and ("NDRB One-Time" not in bcn["bcnTag"]
                                            or "NDRB Recurring" not in bcn["bcnTag"]):
                errors.append(
                    ValidationError(
                        "NDRBs must be tagged as \"NDRB One-Time\" or \"NDRB Recurring\" for output purposes"
                    )
                )
            if bcn["bcnType"] != "Benefit" and "NDRB" in bcn["bcnTag"] or "NDRB One-Time" in bcn["bcnTag"] \
                    or "NDRB Recurring" in bcn["bcnTag"]:
                errors.append(
                    ValidationError(
                        "NDRBs must be a Benefit type BCN"
                    )
                )

        if data["disMag"] or data["riskPref"] or data["confInt"]:
            logger.info("Disaster Magnitude, Risk Preference and Confidence Interval are currently not implemented."
                        "These inputs will have no impact on calculations")

        if errors:
            raise(ValidationError(errors[:NUM_ERRORS_LIMIT]))

        return data
