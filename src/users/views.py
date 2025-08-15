"""Authentication views for user login and logout."""
from __future__ import annotations

from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView


class UserLoginView(DjangoLoginView):
    """Display the login form and authenticate users."""

    template_name = "registration/login.html"
    redirect_authenticated_user = True


class UserLogoutView(DjangoLogoutView):
    """Log out the current user and redirect to the login page."""

    next_page = "users:login"
