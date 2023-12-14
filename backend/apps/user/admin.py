from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from user.models import User


class UserAdmin(BaseUserAdmin):

    fieldsets = (
        (_('User Info'),
            {'fields': (
                "username",
                "first_name",
                "last_name",
                "name",
                "two_step_password",
            )
        }),
        (_('Status/Groups/Permissions'),
            {'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            )
        }),
    )

    add_fieldsets = (
        (_("create new user"), {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
    )

    list_display = (
        'first_name', 'last_name', 'username', 'name',
        'two_step_password', 'is_staff', 'is_superuser', 'is_active',
        'last_login', 'updated_at', 'created_at',
    )
    list_filter = (
        'two_step_password', 'is_staff', 'is_superuser', 'is_active',
        'updated_at', 'created_at',
    )
    ordering = (
        'first_name', 'last_name', 'username', 'name',
        'two_step_password', 'is_staff', 'is_superuser', 'is_active',
        'updated_at', 'created_at',
    )
    list_display_links = ('first_name', 'last_name', 'username', 'name',)
    search_fields = ('first_name', 'last_name', 'username', 'name',)
    filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(User, UserAdmin)
