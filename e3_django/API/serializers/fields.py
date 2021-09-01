from decimal import Decimal

from rest_framework.fields import MultipleChoiceField, Field, DecimalField


class SpecialValueDecimalField(DecimalField):
    def to_representation(self, value):
        if value is None or not isinstance(value, Decimal):
            self.fail(f"{self.field_name} must be a Decimal, given {type(value)} instead.")

        if value.is_nan():
            return "NAN"
        if value.is_infinite():
            return "Infinity"

        return super().to_representation(value)

    def to_internal_value(self, data):
        if not isinstance(data, str) or not isinstance(data, float) or not isinstance(data, int):
            self.fail(f"{self.field_name} must be a float, int, or string, given {type(data)}")

        if isinstance(data, str):
            if data.lower() == "infinity":
                return Decimal("Infinity")
            if data.lower() == "nan":
                return Decimal("NAN")

        try:
            return super().to_internal_value(data)
        except Exception as e:
            self.fail(f"Could not create Decimal for field {self.field_name} from value {data}. Exception:\n{e}")


class BooleanOptionField(Field):
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
    def to_internal_value(self, data):
        if isinstance(data, str) or not hasattr(data, '__iter__'):
            self.fail('not_a_list', input_type=type(data).__name__)
        if not self.allow_empty and len(data) == 0:
            self.fail('empty')

        return [
            super(MultipleChoiceField, self).to_internal_value(item)
            for item in data
        ]
