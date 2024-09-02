# products/urls.py
from django.urls import path
from .views import ProductDetailView
from .views import ProductListCreateView

# from .views import ProductListCreateView, ProductDetailView, CategoryListView

# urlpatterns = [
#     path('categories/', CategoryListView.as_view(), name='category-list'),
# ]



urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

]
