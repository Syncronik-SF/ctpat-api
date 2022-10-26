from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from authentication.models import Profile, WorkerType


@admin.register(get_user_model())
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'first_name', 'last_name', 'job_title', 'phone')
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'first_name', 'last_name', 'job_title', 'phone')
        }),
    )
    

admin.site.register(Profile)
admin.site.register(WorkerType)
