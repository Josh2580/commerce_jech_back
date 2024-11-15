# products/urls.py
from django.urls import path
from .views import ProductDetailView, ProductListCreateView, FeaturedProductListCreateView, FeaturedProductDetailView


urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('featured/', FeaturedProductListCreateView.as_view(), name='featured-products-list'),
    path('featured/<int:pk>/', FeaturedProductDetailView.as_view(), name='featured-product-detail'),

]

