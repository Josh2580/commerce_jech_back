# stores/urls.py
from django.urls import path
from .views import StoreListCreateView, StoreProductListView

urlpatterns = [
    path('', StoreListCreateView.as_view(), name='store-list-create'),
    path('<int:pk>/', StoreProductListView.as_view(), name='store-detail'),
    path('<int:store_pk>/products/', StoreProductListView.as_view(), name='store-product-list'),
]
