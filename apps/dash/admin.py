# register GreekStudyUser
from django.contrib import admin
from .models import GreekStudyUser


# add fields to admin
class GreekStudyUserAdmin(admin.ModelAdmin):
    list_display = ("gs_id", "first", "last")


# add the admin
admin.site.register(GreekStudyUser, GreekStudyUserAdmin)
