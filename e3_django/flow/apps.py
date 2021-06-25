from API.registry import E3AppConfig


class FlowConfig(E3AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'flow'
    verbose_name = 'E3 Flow Summary'

    output = "FlowSummary"

    def analyze(self, baseInput, steps=None):
        print(f"Input on Flow: {baseInput}, steps: {steps}")
        return baseInput
