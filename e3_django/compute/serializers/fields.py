from decimal import Decimal

from rest_framework.fields import MultipleChoiceField, Field, DecimalField


class InfinityDecimalField(DecimalField):
    """
    Custom serializer field that allows for decimals that can be infinity.
    """

    def to_representation(self, value):
        if isinstance(value, Decimal) and value.is_infinite():
            return "Infinity"

        return super().to_representation(value)

    def to_internal_value(self, data):
        if isinstance(data, str) and data.lower() == "infinity":
            return Decimal("Infinity")

        return super().to_internal_value(data)


class BooleanOptionField(Field):
    """
    Custom serializer field that allows for custom true and false sets.
    """

    default_error_messages = {
        'none': 'Original value cannot be None.',
        'invalid': 'Input must be a valid option.'
    }

    def __init__(self, true_values, false_values, **kwargs):
        super().__init__(**kwargs)

        self.original_value = None

        true_values.add(True)
        self.true_values = true_values

        false_values.add(False)
        self.false_values = false_values

    def to_representation(self, value):
        if self.original_value is None:
            self.fail("none")

        return f"{self.original_value}"

    def to_internal_value(self, data):
        self.original_value = data

        if data in self.true_values:
            return True
        elif data in self.false_values:
            return False
        else:
            self.fail("invalid")


class ListMultipleChoiceField(MultipleChoiceField):
    """
    Custom serializer field that allows for multiple choice options in a list.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) or not hasattr(data, '__iter__'):
            self.fail('not_a_list', input_type=type(data).__name__)
        if not self.allow_empty and len(data) == 0:
            self.fail('empty')

        return [
            super(MultipleChoiceField, self).to_internal_value(item)
            for item in data
        ]
