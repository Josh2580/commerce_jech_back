# cart/urls.py
from django.urls import path
from .views import CartRetrieveUpdateView, CartItemCreateView, CartItemUpdateDeleteView

urlpatterns = [
    path('', CartRetrieveUpdateView.as_view(), name='cart-detail'),
    path('items/', CartItemCreateView.as_view(), name='cart-item-create-update'),
    path('items/<int:pk>/', CartItemUpdateDeleteView.as_view(), name='cart-item-delete'),
]
