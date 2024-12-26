from django.contrib import admin
from payments.models import PaymentMethod,  UserPaymentMethod

# Register your models here.
admin.site.register(PaymentMethod)
admin.site.register(UserPaymentMethod)
# admin.site.register(Transaction)
