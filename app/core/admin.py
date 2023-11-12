"""
Django admin customization.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _ # it just takes care of translating titles in the admin panel.

from core import models



class UserAdmin(BaseUserAdmin):
    """defines the admin interface for the User Model."""

    # This is for listing all of the users in the admin panel.
    ordering = ['id']
    list_display = ['email', 'name']

    # This is for specifying the fields in which admin can monitor and change for existing users.
    fieldsets = (
        (None, {'fields': ('email', 'name')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        ),
        (_('Important dates'), {'fields': ('last_login',)})

    )
    readonly_fields = ['last_login']

    # This is for specifying the fields in which admin can add for new users.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )

    

admin.site.register(get_user_model(), UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
