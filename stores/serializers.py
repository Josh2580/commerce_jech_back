# stores/serializers.py
from rest_framework import serializers
from .models import Store
from products.serializers import ProductSerializer



class StoreSerializer(serializers.ModelSerializer):
    # products = ProductSerializer(many=True, read_only=True)
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ['id', 'name', 'description', 'logo', 'image_url', 'created_at', 'updated_at', 'products']
