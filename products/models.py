# products/models.py
import uuid
from django.db import models
from django.utils.text import slugify
from stores.models import Store
from categories.models import Category
from django.conf import settings
from django.utils import timezone



class Product(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    old_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    store = models.ForeignKey(Store, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_sales = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name
    
       
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/products/images/default-product.jpg'  # Fallback to default image if no image is provided
 

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            counter = 1
            while Product.objects.filter(owner=self.owner, slug=slug).exists():
                slug = f'{slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    

class FeaturedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='featured_products')
    start_date = models.DateTimeField(null=True, blank=True)
    featured_image = models.ImageField(upload_to='featured/products/', blank=True, null=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Featured Product: {self.product.name}"
    
    def main_product(self):
        """Returning the source/main product name"""
        id = self.product.product_id
        name = self.product.name
        slug = self.product.slug
        price = self.product.price
        old_price = self.product.old_price
        image_url = self.product.image_url
        return {"id":id, "name":name, "slug":slug,"price":price,"old_price":old_price, "image_url":image_url}
    
    def is_active(self):
        """Check if the product is currently featured based on the start and end date."""
        now = timezone.now()
        return (self.start_date is None or self.start_date <= now) and (self.end_date is None or self.end_date >= now)
        # return (self.start_date <= now) and (self.end_date >= now)

