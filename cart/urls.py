# cart/urls.py
from django.urls import path
from .views import CartRetrieveUpdateView, CartItemCreateUpdateDeleteView

urlpatterns = [
    path('', CartRetrieveUpdateView.as_view(), name='cart-detail'),
    path('items/', CartItemCreateUpdateDeleteView.as_view(), name='cart-item-create-update'),
    path('items/<int:pk>/', CartItemCreateUpdateDeleteView.as_view(), name='cart-item-delete'),
]
