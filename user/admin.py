from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'phone_number', 'score', 'mycode', 'is_premium', 'is_staff', 'is_active']
    ordering = ['id', '-score']
    search_fields = ['phone_number', 'score', 'referrer', 'first_name', 'is_premium']
    list_filter = ['score', 'phone_number', 'first_name']
    fieldsets = (
        (None, {
            'fields': ('first_name', 'phone_number', 'score', 'referrer', 'balance', 'mycode', 'is_premium', 'is_staff', 'is_active'),
        }),
    )
