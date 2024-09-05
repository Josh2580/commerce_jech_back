# orders/urls.py
from django.urls import path
from .views import OrderCreateView, OrderListView, OrderDetailView

urlpatterns = [
    path('', OrderListView.as_view(), name='order-list'),
    path('create/', OrderCreateView.as_view(), name='order-create'),
    path('<uuid:order_id>/', OrderDetailView.as_view(), name='order-detail'),
    # path('<int:id>/', OrderDetailView.as_view(), name='order-detail'),
]
