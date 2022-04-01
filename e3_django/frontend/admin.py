from django.contrib import admin
from rest_framework_api_key.admin import APIKeyModelAdmin

from frontend.models import UserAPIKey, EmailUser


@admin.register(UserAPIKey)
class UserAPIKeyModelAdmin(APIKeyModelAdmin):
    pass


@admin.register(EmailUser)
class EmailUserModelAdmin(admin.ModelAdmin):
    pass
