from django.contrib import admin

# Register your models here.
from .models import User, Food

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Food)    
class FoodAdmin(admin.ModelAdmin):
    list_display = (
        'description',
        'serving_size',
        'estimated_calories',
        'created_at',
        'updated_at',
    )
    list_display_links = ('description', 'serving_size')
    search_fields = ('description', 'details')



@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields for editing an existing user
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('middle_name', 'address', 'occupation', 'date_of_birth')}),
    )

    # Fields for creating a new user in the admin
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Extra Info', {'fields': ('middle_name', 'address', 'occupation', 'date_of_birth')}),
    )

    # Show in the list display
    list_display = BaseUserAdmin.list_display + ('middle_name', 'occupation', 'date_of_birth')

    search_fields = BaseUserAdmin.search_fields + ('middle_name', 'occupation')