# categories/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subcategories', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def is_root_category(self):
        return self.parent is None
