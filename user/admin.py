from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['id', 'first_name', 'phone_number', 'created_at', 'is_superuser', 'is_staff', 'is_active']
    ordering = ['id']
    add_fieldsets = (
        (None, {
            'fields': ('phone_number', 'is_superuser'),
        }),
    )
    fieldsets = (
        (None, {
            "fields": (
                ('first_name', 'phone_number', 'mycode', 'is_premium'),
            ),
        }),
    )


admin.site.register(CustomUser, CustomUserAdmin)
