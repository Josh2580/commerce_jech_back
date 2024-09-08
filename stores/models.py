# stores/models.py
from django.db import models
from django.conf import settings

class Store(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='stores', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='stores/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    @property
    def image_url(self):
        if self.logo and hasattr(self.logo, 'url'):
            return self.logo.url
        return '/static/stores/images/default-store.jpg'  # Fallback to default image if no image is provided
 

    @property
    def product_count(self):
        return self.products.count()
