from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from abstractuser.models import User


class AbstractAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {"fields": (
                ("last_name", "first_name"),
                ("email", "is_superuser"),
                ("is_active", "is_staff")
            )}
        ),
        (
            _("Groups"),
            {
                "classes": ('collapse',),
                "fields": (
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (
            _("Important dates"),
            {
                "classes": ('collapse',),
                "fields": ("last_login", "date_joined")
            }
        ),
        (
            _("Profile"),
            {
                "fields": ("rank",)
            }
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )
    readonly_fields = ('username', 'is_superuser')


admin.site.register(User, AbstractAdmin)
