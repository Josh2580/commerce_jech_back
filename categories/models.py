# categories/models.py
from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    image = models.ImageField(upload_to='categorys/images/', blank=True, null=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subcategories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # if self.parent and self.parent.parent is not None:
        #     raise ValidationError(f"A subcategory cannot use another subcategory {self.parent.name} as its parent.")

        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_root_category(self):
        return self.parent is None
    
    @property
    def image_url(self):
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        return '/static/categorysimages/default-category.png'  # Fallback to default image if no image is provided
 