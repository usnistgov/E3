from rest_framework.fields import ListField
from rest_framework.serializers import Serializer

from API.objects.Alternative import Alternative
from API.objects.Analysis import Analysis
from API.objects.Bcn import Bcn
from API.objects.Input import Input
from API.serializers.AlternativeSerializer import AlternativeSerializer
from API.serializers.AnalysisSerializer import AnalysisSerializer
from API.serializers.BcnSerializer import BCNSerializer
from API.serializers.SenarioSerializer import ScenarioSerializer
from API.serializers.SensitivitySerializer import SensitivitySerializer


class InputSerializer(Serializer):
    analysisObject = AnalysisSerializer(required=True)
    alternativeObjects = ListField(child=AlternativeSerializer(), required=True)
    bcnObjects = ListField(child=BCNSerializer(), required=True)
    sensitivityObject = SensitivitySerializer(required=False)
    scenarioObject = ScenarioSerializer(required=False)

    def create(self, validated_data):
        analysis = Analysis(**validated_data.pop("analysisObject"))

        return Input(
            analysis,
            [Alternative(**data) for data in validated_data.pop("alternativeObjects")],
            [Bcn(analysis.studyPeriod, **data) for data in validated_data.pop("bcnObjects")],
            None,
            None,
        )

    def update(self, instance, validate_data):
        instance.analysis = validate_data.get("analysisObject", instance.analysis)
        instance.alternatives = validate_data.get("alternativeObjects", instance.alternatives)
        instance.bcns = validate_data.get("bcnObjects", instance.bcns)
        instance.sensitivity = validate_data.get("sensitivityObject", instance.sensitivity)
        instance.scenario = validate_data.get("scenarioObject", instance.scenario)

        return instance
