# cart/serializers.py
from rest_framework import serializers
from .models import Cart, CartItem
from products.serializers import ProductSerializer
from products.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_data', 'quantity', 'subtotal', 'added_at']
    
    # def update(self, instance, validated_data):
    #     # Handle partial updates safely
    #     for attr, value in validated_data.items():
    #         setattr(instance, attr, value)
    #     instance.save()
    #     return instance

 

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'session_key', 'items', 'get_total', 'created_at', 'updated_at']

   
