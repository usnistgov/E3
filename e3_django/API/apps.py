from django.apps import AppConfig

from API import registry


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'API'

    def ready(self):
        registry.init()
