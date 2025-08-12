from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, University

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'full_name', 'user_type', 'is_verified_seller', 'is_active')
    list_filter = ('user_type', 'is_verified_seller', 'is_active')
    search_fields = ('email', 'full_name', 'phone_number')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'phone_number', 'university', 'profile_image')}),
        ('Permissions', {'fields': ('user_type', 'is_verified_seller', 'is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'full_name', 'phone_number', 'university', 'password1', 'password2'),
        }),
    )

class UniversityAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_verified')
    search_fields = ('name',)
    list_editable = ('is_verified',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(University, UniversityAdmin)