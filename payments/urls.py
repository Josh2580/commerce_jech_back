from django.urls import path
from .views import (
    PaymentMethodListView,
    UserPaymentMethodListCreateView, TransactionListView, InitializePaymentView, VerifyTransactionView
)

urlpatterns = [
    path('methods/', PaymentMethodListView.as_view(), name='payment-method-list'),
    path('user-methods/', UserPaymentMethodListCreateView.as_view(), name='user-payment-method-list-create'),
    path('transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('initialize/', InitializePaymentView.as_view(), name='initialize_payment'),
    path('verify/', VerifyTransactionView.as_view(), name='verify_transaction'),
]

