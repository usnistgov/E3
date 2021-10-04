from rest_framework.fields import ListField

from API.registry import E3AppConfig
from compute.objects import OptionalCashFlow
from compute.serializers import OptionalCashFlowSerializer


class OptionalCashFlowConfig(E3AppConfig):
    name = "compute.optional"
    verbose_name = 'E3 Optional Cash Flow Object'

    depends_on = ["internal:cash-flows"]
    output = "OptionalSummary"
    serializer = ListField(child=OptionalCashFlowSerializer(), required=False)

    def analyze(self, base_input, steps=None):
        def create_empty_tag_flows(user_input):
            """
            Generate empty cash flows for every tag in the bcn object set.

            :param user_input: The input object.
            :return: A dict of (alt, tag) to empty cash flows for every tag for every bcn.
            """
            result = {}

            for bcn in user_input.bcnObjects:
                for tag in bcn.bcnTag:
                    if not tag:
                        continue

                    for alt_id in bcn.altID:
                        key = (alt_id, tag)

                        if key in result:
                            continue

                        result[key] = OptionalCashFlow(alt_id, tag, bcn.quantUnit,
                                                       user_input.analysisObject.studyPeriod)

            return result

        def calculate_tag_flows(flows, user_input):
            """
            Calculate cash flows for all tags in bcn set.

            :param flows: The cash flows calculated from the bcn objects.
            :param user_input: The input object.
            :return: A list of cash flows for all tags. Some flows may be empty for some alternatives.
            """
            optionals = create_empty_tag_flows(user_input)

            for bcn in user_input.bcnObjects:
                for tag in bcn.bcnTag:
                    if not tag:
                        continue

                    for alt in bcn.altID:
                        key = (alt, tag)
                        optionals[key].add(bcn, flows[bcn])

            return list(optionals.values())

        return calculate_tag_flows(steps[0], base_input)

