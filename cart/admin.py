from django.contrib import admin
from cart.models import Cart, CartItem

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'session_key')
    # prepopulated_fields = {'slug': ('name',)}  # Optionally prepopulate slug in the admin



admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem)
