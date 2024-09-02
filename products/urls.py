# products/urls.py
from django.urls import path
# from .views import ProductListCreateView, ProductDetailView, CategoryListView

# urlpatterns = [
#     path('products/', ProductListCreateView.as_view(), name='product-list'),
#     path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
#     path('categories/', CategoryListView.as_view(), name='category-list'),
# ]


from .views import ProductCreateView

urlpatterns = [
    path('create/', ProductCreateView.as_view(), name='product-create'),
]
