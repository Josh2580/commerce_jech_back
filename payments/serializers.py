from rest_framework import serializers
from payments.models_methods import PaymentMethod, UserPaymentMethod
from django.contrib.auth import get_user_model
from payments.models import Transaction
from users.serializers import UserSerializer
from orders.models import Order
# from orders.serializers import OrderSerializer

User = get_user_model()

class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = '__all__'

class UserPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPaymentMethod
        fields = '__all__'
        

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    # order = OrderSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'tx_ref', 'amount', 'status', 'created_at', 'order']
        read_only_fields = ['tx_ref', 'status', 'created_at', 'order']

