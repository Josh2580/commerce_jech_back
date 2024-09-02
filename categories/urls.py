# categories/urls.py
from django.urls import path
from .views import CategoryCreateView, CategoryListView

urlpatterns = [
    path('', CategoryListView.as_view(), name='category-list'),
    path('create/', CategoryCreateView.as_view(), name='category-create'),
]
