from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ['username', 'email', 'phone_number']
    list_display_links = ['username', 'email', 'phone_number']
    # list_display = UserAdmin.list_display[:4] + ('nat_code', 'gender', 'phone_number') + UserAdmin.list_display[4:]
    # list_display_links = UserAdmin.list_display[:4] + ('nat_code', 'gender', 'phone_number') + UserAdmin.list_display[4:]
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "gender",
                    "first_name",
                    "last_name",
                    "nat_code", 
                    "phone_number", 
                    "email"
                ),
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = fieldsets[0:2]
