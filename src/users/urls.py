"""URL routing for user authentication views."""
from __future__ import annotations

from django.urls import path

from .views import UserLoginView, UserLogoutView

app_name = "users"

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
]
