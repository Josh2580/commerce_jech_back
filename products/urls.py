# products/urls.py
from django.urls import path, include
from rest_framework_nested import routers
from .views import ProductViewSet, FeaturedProductListCreateView, FeaturedProductDetailView
from reviews.views import ReviewViewSet

# Root router for products
router = routers.SimpleRouter()
router.register(r'', ProductViewSet, basename='products')

# # Nested router for product reviews
product_review_router = routers.NestedSimpleRouter(router, r'', lookup='product')
product_review_router.register(r'reviews', ReviewViewSet, basename='product-reviews')


urlpatterns = [
    path('featured/', FeaturedProductListCreateView.as_view(), name='featured-products-list'),
    path('featured/<int:pk>/', FeaturedProductDetailView.as_view(), name='featured-product-detail'),
    path('', include(router.urls)),
    path('', include(product_review_router.urls)),

]


