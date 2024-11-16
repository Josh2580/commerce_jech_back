from django.contrib import admin
from .models import Category
from .form import CategoryAdminForm


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm

    list_display = ('name', 'parent', 'image_url', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Optionally prepopulate slug in the admin




admin.site.register(Category, CategoryAdmin)
