import logging

from rest_framework.exceptions import ValidationError
from rest_framework.fields import ListField
from rest_framework.serializers import Serializer

from API.objects import Input, Analysis, Alternative, Bcn
from API.serializers import AnalysisSerializer, AlternativeSerializer, BCNSerializer, SensitivitySerializer, \
    ScenarioSerializer


class InputSerializer(Serializer):
    """
    Object serializer for main input object.
    """

    analysisObject = AnalysisSerializer(required=True)
    alternativeObjects = ListField(child=AlternativeSerializer(), required=True)
    bcnObjects = ListField(child=BCNSerializer(), required=True)
    sensitivityObject = SensitivitySerializer(required=False)
    scenarioObject = ScenarioSerializer(required=False)

    def validate(self, data):
        study_period = data["analysisObject"]["studyPeriod"]
        for bcn in data["bcnObjects"]:
            quant_var_value = bcn["quantVarValue"]
            recur_var_value = bcn["recurVarValue"]

            if quant_var_value is not None and isinstance(quant_var_value, list) and \
                    len(quant_var_value) != study_period:
                raise ValidationError(f"The length of quantVarValue for BCN {bcn['bcnID']} is not equal to the study "
                                      f"period {study_period}. Given {quant_var_value}")

            if recur_var_value is not None and isinstance(recur_var_value, list) and \
                    len(recur_var_value) != study_period:
                raise ValidationError(f"The length of recurVarValue for BCN {bcn['bcnID']} is not equal to the study "
                                      f"period {study_period}. Given {recur_var_value}")

        # Ensure that only one alternative has baselineBool = True.
        if len([x for x in data["alternativeObjects"] if x["baselineBool"]]) != 1:
            raise ValidationError("Only one alternative can be the baseline")

        return data

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
