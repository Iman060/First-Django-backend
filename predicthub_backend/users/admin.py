from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'total_points', 'win_rate', 'streak', 'created_at']
    list_filter = ['is_staff', 'is_superuser', 'created_at']
    search_fields = ['username', 'email']
    ordering = ['-total_points']
    readonly_fields = ['created_at']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Prediction Market Stats', {
            'fields': ('total_points', 'win_rate', 'streak')
        }),
    )

