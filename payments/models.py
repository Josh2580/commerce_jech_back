from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings



class PaymentMethod(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='payment/', blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class UserPaymentMethod(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payment_methods')
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.CASCADE)
    details = models.JSONField(null=True, blank=True)  # Example: {"card_last4": "1234"}
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.payment_method.name}"


# class Transaction(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='transactions')
#     payment_method = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, null=True, blank=True)
#     transaction_ref = models.CharField(max_length=100, unique=True)
#     status = models.CharField(max_length=50, default='Pending')
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Transaction {self.transaction_ref} - {self.status}"
