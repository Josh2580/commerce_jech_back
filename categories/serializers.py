# categories/serializers.py
from rest_framework import serializers
from .models import Category
from products.serializers import ProductSerializer

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    # products = ProductSerializer(many=True, read_only=True)
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'is_root_category', 'image_url', 'image', 'slug',  'parent', 'subcategories', 'products',]

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data

class CategorySerializerList(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'is_root_category', 'image_url', 'image', 'slug',  'parent', 'subcategories']

    def get_subcategories(self, obj):
        return CategorySerializerList(obj.subcategories.all(), many=True).data
