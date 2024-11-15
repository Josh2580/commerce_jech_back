# products/serializers.py
from rest_framework import serializers
from .models import Product, FeaturedProduct
from rest_framework.exceptions import ValidationError

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'product_id', 'name', 'owner', 'slug', 'price', 'old_price', 'total_sales', 'stock', 'store', 'categories', 'image', 'image_url', 'description', 'created_at', 'updated_at']
    
    def validate_categories(self, categories):
        # Check if any of the categories are root categories (no parent)
        root_categories = categories.filter(parent=None)
        if root_categories.exists():
            # Collect their names
            category_names = ", ".join([cat.name for cat in root_categories])
            raise ValidationError(
                f"Product cannot be associated with root categories. "
                f"The following categories are root categories: {category_names}. "
                f"Please assign valid subcategories."
            )
        return categories



class FeaturedProductSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    # product_name = serializers.SerializerMethodField()

    class Meta:
        model = FeaturedProduct
        fields = ['id', 'main_product', 'featured_image', 'is_active', 'product',  'start_date', 'end_date', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    # def get_product_name(self, obj):
    #     return obj.main_product_name()
    
    # def create(self, validated_data):
    #     return FeaturedProduct.objects.create(**validated_data)

    

    

