from django.contrib import admin
from payments.models_methods import PaymentMethod,  UserPaymentMethod
from payments.models import Transaction

# Register your models here.
admin.site.register(PaymentMethod)
admin.site.register(UserPaymentMethod)
admin.site.register(Transaction)
