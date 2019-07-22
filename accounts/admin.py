from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Profile


class CustomeAdmin(UserAdmin):
    list_display = ('email', 'is_active', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Important Dates', {'fields': ('last_login',)}),
        ('Permissions', {'fields': ('is_active', 'is_buser', 'is_staff', 'is_admin')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(get_user_model(), CustomeAdmin)
admin.site.unregister(Group)

admin.site.register(Profile)
