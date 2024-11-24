# products/urls.py
from django.urls import path, include
from rest_framework_nested import routers
from .views import ProductViewSet, FeaturedProductListCreateView, FeaturedProductDetailView

# Root router for categories
router = routers.SimpleRouter()
router.register(r'', ProductViewSet, basename='products')

urlpatterns = [
    path('featured/', FeaturedProductListCreateView.as_view(), name='featured-products-list'),
    path('featured/<int:pk>/', FeaturedProductDetailView.as_view(), name='featured-product-detail'),
    path('', include(router.urls)),

]


