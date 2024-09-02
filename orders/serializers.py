# orders/serializers.py
from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from products.models import Product

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'price']
        read_only_fields = ['id', 'price']
    
    def create(self, validated_data):
        product = validated_data['product']
        quantity = validated_data.get('quantity', 1)
        price = product.price  # Capture the price at the time of order
        return OrderItem.objects.create(product=product, quantity=quantity, price=price, **validated_data)

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'items', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'status', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        user = self.context['request'].user
        order = Order.objects.create(user=user, **validated_data)
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        return order
    
    def update(self, instance, validated_data):
        # Handle updates if necessary (e.g., changing status)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance
