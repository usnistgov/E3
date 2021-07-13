from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin

from frontend.models import UserAPIKey


@admin.register(UserAPIKey)
class UserAPIKeyModelAdmin(APIKeyModelAdmin):
    pass
