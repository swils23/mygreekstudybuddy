from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class UserAdmin(UserAdmin):
    # list_display = UserAdmin.list_display + ("gs_userID", "gs_email", "gs_password")
    fieldsets = UserAdmin.fieldsets + (("GreekStudy", {"fields": ("gs_userID", "gs_email", "gs_password", "hours")}),)


admin.site.register(User, UserAdmin)
