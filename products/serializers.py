# # products/serializers.py

# class ProductSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'category_id', 'image', 'created_at', 'updated_at']

# products/serializers.py
from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'product_id', 'name', 'owner', 'slug', 'description', 'price', 'stock', 'store', 'categories', 'image', 'created_at', 'updated_at']
