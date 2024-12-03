from django.contrib import admin
from .models import Review


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'rating', 'product', 'updated_at')

admin.site.register(Review, ReviewAdmin)