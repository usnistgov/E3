from rest_framework.fields import ListField
from API.registry import E3ModuleConfig
from e3_django.API.serializers.SensitivitySerializer import SensitivitySerializer


class SensitivityConfig(E3ModuleConfig):
    """
    This module calculates the sensitivity objects from BCN objects.
    """

    name = "compute.sensitivity"
    verbose_name = 'E3 Sensitivity Generator'

    output = "sensitivity-summary"
    serializer = ListField(child=SensitivitySerializer(), required=False)

    def run(self, base_input, dependencies=None):

        return [x for x in base_input.sensitivityObjects.calculateOutput()]