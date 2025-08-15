"""Admin configuration for the custom User model."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define admin model for custom User with role field."""

    fieldsets = BaseUserAdmin.fieldsets + (("Role", {"fields": ("role",)}),)
    add_fieldsets = BaseUserAdmin.add_fieldsets + ((None, {"fields": ("role",)}),)
    list_display = ("username", "email", "role", "is_staff")
    list_filter = (*BaseUserAdmin.list_filter, "role")
    search_fields = ("username", "email")
    ordering = ("username",)

