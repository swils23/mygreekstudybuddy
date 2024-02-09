from typing import Union

from django.conf import settings
from django.contrib import admin
from django.urls import URLPattern, URLResolver, include, path

from apps.accounts.views import NameChange
from apps.base.views import IndexView, http_404, http_500
from apps.dash.views import (
    GreekStudyAccountSetupView,
    GreekStudyHoursView,
    GreekStudyIndexView,
    GreekStudyUsersView,
    TaskGetUserIDView,
)

# Includes
urlpatterns: list[Union[URLResolver, URLPattern]] = [path(r"admin/", admin.site.urls)]

# Project Urls
urlpatterns += [
    path("", IndexView.as_view(), name="site_index"),
    path("-/", include("django_alive.urls")),
    path("500/", http_500),
    path("404/", http_404),
    path("accounts/name/", NameChange.as_view(), name="account_change_name"),
    path("accounts/", include("allauth.urls")),
    path("dash/", GreekStudyIndexView.as_view(), name="dash_index"),
    path("greekstudy-account/", GreekStudyAccountSetupView.as_view(), name="greekstudy_account"),
    path("hours/", GreekStudyHoursView.as_view(), name="hours"),
    path("get-user-id/", TaskGetUserIDView.as_view(), name="get-user-id"),
    path("users/", GreekStudyUsersView.as_view(), name="users"),
]

# Debug/Development URLs
if settings.DEBUG is True:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
        path("admin/doc/", include("django.contrib.admindocs.urls")),
    ]
