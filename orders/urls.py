# orders/urls.py
from django.urls import path
from .views import OrderView, OrderDetailView, OrderItemView

urlpatterns = [
    path('', OrderView.as_view(), name='order-create'),
    # path('<uuid:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('items/', OrderItemView.as_view(), name='order-item'),
]
