# categories/serializers.py
from rest_framework import serializers
from .models import Category
from products.serializers import ProductSerializer

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    products = ProductSerializer(many=True, read_only=True)
    # products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'is_root_category', 'image_url', 'image', 'slug',  'parent', 'subcategories', 'products',]

    def get_subcategories(self, obj):
        return CategorySerializer(obj.subcategories.all(), many=True).data
    
    def validate_parent(self, value):
        """
        Validate that a subcategory cannot have another subcategory as its parent.
        """
        if value and value.parent is not None:  # Check if parent exists and is itself a subcategory
            raise serializers.ValidationError(
                f"A subcategory cannot use another subcategory ('{value.name}') as its parent."
            )
        return value

class CategorySerializerList(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'is_root_category', 'image_url', 'image', 'slug',  'parent', 'subcategories']

    def get_subcategories(self, obj):
        return CategorySerializerList(obj.subcategories.all(), many=True).data
