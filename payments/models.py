 
from django.db import models
from django.conf import settings

from orders.models import Order
from payments.models_methods import PaymentMethod


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_transactions', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_transactions')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
    tx_ref = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=50, default='Pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction {self.tx_ref} - {self.status} Transaction_ID : {self.id}"
