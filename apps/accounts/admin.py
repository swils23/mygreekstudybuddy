from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User

# add gs_userID to admin


class UserAdmin(UserAdmin):
    # list_display = UserAdmin.list_display + ("gs_userID", "gs_email", "gs_password")
    fieldsets = UserAdmin.fieldsets + (("Greek Study", {"fields": ("gs_userID", "gs_email", "gs_password")}),)


admin.site.register(User, UserAdmin)
