# products/models.py
import uuid
from django.db import models
from django.utils.text import slugify
from stores.models import Store
from categories.models import Category
from django.conf import settings



class Product(models.Model):
    product_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    store = models.ForeignKey(Store, related_name='products', on_delete=models.SET_NULL, null=True)
    categories = models.ManyToManyField(Category, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = slugify(self.name)
            counter = 1
            while Product.objects.filter(owner=self.owner, slug=slug).exists():
                slug = f'{slug}-{counter}'
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
