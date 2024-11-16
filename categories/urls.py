from django.urls import path, include
from rest_framework_nested import routers
from .views import CategoryViewset
from products.views import ProductViewSet  # Assuming you have a ProductViewSet

# Root router for categories
router = routers.SimpleRouter()
router.register(r'', CategoryViewset, basename='categories')

# Nested router for subcategories under categories
subcategory_router = routers.NestedSimpleRouter(router, r'', lookup='category')
subcategory_router.register(r'subcategories', CategoryViewset, basename='category-subcategories')

# Nested router for products under subcategories
product_router = routers.NestedSimpleRouter(subcategory_router, r'subcategories', lookup='subcategory')
product_router.register(r'products', ProductViewSet, basename='subcategory-products')

# Include all routers in the URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('', include(subcategory_router.urls)),
    path('', include(product_router.urls)),
]


