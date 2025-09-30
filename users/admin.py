from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('email', 'role', 'first_name','last_name','is_staff', 'is_verified')
    list_filter = ('role', 'is_staff', 'is_verified')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('role', 'is_staff', 'is_superuser', 'is_verified', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'role', 'is_staff', 'is_superuser', 'is_verified'),
        }),
    )

    ordering = ('email',)
    search_fields = ('email', 'role')

admin.site.register(User, CustomUserAdmin)
