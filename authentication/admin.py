from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from authentication.models import Profile


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    pass

admin.site.register(Profile)