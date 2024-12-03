from django.db import models

# Create your models here.
from django.db import models
from products.models import Product
from django.conf import settings


class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()  # Rating out of 5
    content = models.TextField(max_length=500)  # Optional review content
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Review by {self.user} for {self.product.name} ({self.rating}/5)"


    @property
    def reviewer_names(self):
        name = {"first_name":self.user.first_name, "last_name":self.user.last_name}
        return name
