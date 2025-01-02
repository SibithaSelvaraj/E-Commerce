from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Correct import for your User model

class CustomUserAdmin(UserAdmin):
    model = User  # Use the correct model name
    # Optional: Configure fields for admin view
    list_display = ['username', 'email', 'phone_number', 'address']
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_number', 'address')}),
    )

admin.site.register(User, CustomUserAdmin)
