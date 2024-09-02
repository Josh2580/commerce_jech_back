# # products/serializers.py
# from rest_framework import serializers
# from .models import Product, Category

# class CategorySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ['id', 'name', 'slug']

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
    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'stock', 'store', 'categories', 'image', 'created_at', 'updated_at']
