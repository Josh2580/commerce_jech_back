# categories/urls.py
from django.urls import path, include
from rest_framework_nested import routers
# from .views import CategoryCreateView, CategoryListView, CategoryDetailView
from .views import CategoryViewset, ProductViewSet

# urlpatterns = [
#     path('', CategoryListView.as_view(), name='category-list'),
#     path('create/', CategoryCreateView.as_view(), name='category-create'),
#     path('<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
# ]

# Create the root router
router = routers.SimpleRouter()
router.register(r'categories', CategoryViewset)

# Create the nested router for products under categories
category_router = routers.NestedSimpleRouter(router, r'categories', lookup='category')
category_router.register(r'products', ProductViewSet, basename='category-products')

# Include the routers in your URL patterns
urlpatterns = [
    path('', include(router.urls)),
    path('', include(category_router.urls)),
]
