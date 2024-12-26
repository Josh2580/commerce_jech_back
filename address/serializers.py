from rest_framework import serializers
from .models import Address

class AddressSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.id')
    class Meta:
        model = Address
        fields = [
            'id', 'user', 'full_name', 'email', 'order_address', 'owner_info', 'phone', 'address_line1', 
            'address_line2', 'city', 'state', 'postal_code', 
            'country', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'id']
