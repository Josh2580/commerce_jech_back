# products/admin.py
from django.contrib import admin
from .models import Product, FeaturedProduct
from .form import ProductAdminForm

class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('id', 'product_id', 'name', 'price', 'store', 'slug')
    prepopulated_fields = {'slug': ('name',)}  # Optionally prepopulate slug in the admin

admin.site.register(Product, ProductAdmin)

class FeaturedProductAdmin(admin.ModelAdmin):
    list_display = ('product__id', 'is_active', 'start_date', 'end_date')
    

admin.site.register(FeaturedProduct, FeaturedProductAdmin)