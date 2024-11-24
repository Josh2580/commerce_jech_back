# stores/urls.py
# from django.urls import path
# from .views import StoreListCreateView, StoreProductListView

# urlpatterns = [
#     path('', StoreListCreateView.as_view(), name='store-list-create'),
#     path('<int:pk>/', StoreProductListView.as_view(), name='store-detail'),
#     path('<int:store_pk>/products/', StoreProductListView.as_view(), name='store-product-list'),
# ]

from django.urls import path, include
from rest_framework_nested import routers
from .views import StoreViewset
from products.views import ProductViewSet  # Assuming you have a ProductViewSet

# Root router for categories
router = routers.SimpleRouter()
router.register(r'', StoreViewset, basename='stores')

# Nested router for subcategories under categories
store_router = routers.NestedSimpleRouter(router, r'', lookup='store')
store_router.register(r'products', ProductViewSet, basename='store-products')

# Include all routers in the URL patterns
urlpatterns = [
    path('', include(router.urls) ),
    path('', include(store_router.urls)),


]