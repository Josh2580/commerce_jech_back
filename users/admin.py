from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class UserAdmin(BaseUserAdmin):
    # Define the fields to be used in displaying the User model.
    # You might use 'email' instead of 'username'
    ordering = ['email']  # Replace 'username' with 'email' or your primary identifier
    list_display = ['email', 'email_verified', 'first_name', 'last_name', 'is_staff']  # Customize this as needed

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'profile_picture')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    # If you have changed username to email, you'll need to adjust add_fieldsets too
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    form = UserChangeForm
    add_form = UserCreationForm

    # Update the search_fields as well
    search_fields = ('email', 'first_name', 'last_name')

admin.site.register(User, UserAdmin)
