import logging

from rest_framework.exceptions import ValidationError
from rest_framework.fields import ListField
from rest_framework.serializers import Serializer

from API.variables import NUM_ERRORS_LIMIT
from API.objects import Input, Analysis, Alternative, Bcn, Sensitivity
from API.serializers import AnalysisSerializer, AlternativeSerializer, BCNSerializer, SensitivitySerializer, \
    ScenarioSerializer


class InputSerializer(Serializer):
    """
    Object serializer for main input object.
    """

    analysisObject = AnalysisSerializer(required=True)
    alternativeObjects = ListField(child=AlternativeSerializer(), required=True)
    bcnObjects = ListField(child=BCNSerializer(), required=True)
    sensitivityObjects = ListField(child=SensitivitySerializer(required=False), required=False)
    scenarioObject = ScenarioSerializer(required=False)

    def validate(self, data):
        errors = []

        study_period = data["analysisObject"]["studyPeriod"]
        for bcn in data["bcnObjects"]:
            if "quantVarValue" in bcn and bcn["quantVarValue"] is not None:
                quant_var_value = bcn["quantVarValue"]

                try:
                    assert (isinstance(quant_var_value, list) and len(quant_var_value) == study_period + 1) \
                        or (quant_var_value is not None)
                except:
                    errors.append(
                        ValidationError(
                            f"The length of quantVarValue for BCN {bcn['bcnID']} is not equal to the study "
                            f"period {study_period + 1}. Given {quant_var_value}"
                        )
                    )

            if bcn["recurBool"] is True and bcn["recurVarValue"] is not None:
                recur_var_value = bcn["recurVarValue"]

                try:
                    assert (isinstance(recur_var_value, list) and len(recur_var_value) == study_period + 1) \
                        or recur_var_value is not None
                except:
                    errors.append(
                        ValidationError(
                            f"The length of recurVarValue for BCN {bcn['bcnID']} is not equal to the study "
                            f"period {study_period + 1}. Given {recur_var_value}"
                        )
                    )

        # Ensure that only one alternative has baselineBool = True.
        try:
            assert len([x for x in data["alternativeObjects"] if x["baselineBool"]]) == 1
        except:
            errors.append(
                ValidationError("Only one alternative can be the baseline.")
            )

 #       if data['sensitivityObjects'] is not None:
 #           # Check bcnID references an existing BCN object
 #           bcnIDList = []
 #           for bcn in data['bcnObjects']:
 #               bcnIDList.append(bcn['bcnID'])
 #
 #           for sensitivity_object in data['sensitivityObjects']:
 #               if sensitivity_object['bcnID'] not in bcnIDList:
 #                   errors.append(ValidationError("bcnID does not correspond to a valid bcn object"))

        if errors:
            raise(ValidationError(errors[:NUM_ERRORS_LIMIT])) # Throws up to NUM_ERRORS_LIMIT number of errors.

        return data

    def create(self, validated_data):
        analysis = Analysis(**validated_data.pop("analysisObject"))
        bcn_cache = {}
        for data in validated_data.pop("bcnObjects"):
            bcn_cache[data["bcnID"]] = Bcn(analysis.studyPeriod, **data)

        for sens_data in validated_data.get("sensitivityObjects", []):
            if sens_data['globalVarBool'] is False:
                Sensitivity(bcnObj=bcn_cache[sens_data["bcnID"]].bcnName, **sens_data)

        return Input(
            analysis,
            [Alternative(**data) for data in validated_data.pop("alternativeObjects")],
            list(bcn_cache.values()),
            [Sensitivity(bcnObj=None, **sens_data) for sens_data in validated_data.get("sensitivityObjects", [])],
            None,
        )

    def update(self, instance, validate_data):
        instance.analysis = validate_data.get("analysisObject", instance.analysis)
        instance.alternatives = validate_data.get("alternativeObjects", instance.alternatives)
        instance.bcns = validate_data.get("bcnObjects", instance.bcns)
        instance.sensitivity = validate_data.get("sensitivityObjects", instance.sensitivity)
        instance.scenario = validate_data.get("scenarioObject", instance.scenario)

        return instance
