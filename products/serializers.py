# # products/serializers.py

# class ProductSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(read_only=True)
#     category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'description', 'price', 'stock', 'category', 'category_id', 'image', 'created_at', 'updated_at']

# products/serializers.py
from rest_framework import serializers
from .models import Product, FeaturedProduct

class ProductSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.id')
    slug = serializers.SlugField(read_only=True)
    class Meta:
        model = Product
        fields = ['id', 'product_id', 'name', 'owner', 'slug', 'price', 'old_price', 'total_sales', 'stock', 'store', 'categories', 'image', 'image_url', 'description', 'created_at', 'updated_at']



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

    

    

