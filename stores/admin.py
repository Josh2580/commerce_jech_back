from django.contrib import admin
from .models import Store


class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'product_count', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Optionally prepopulate slug in the admin

admin.site.register(Store, StoreAdmin)



