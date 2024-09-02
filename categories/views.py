# categories/views.py
from rest_framework import generics, permissions
from .models import Category
from .serializers import CategorySerializer

class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]  # Example permission

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.filter(parent=None)  # Root categories only
    serializer_class = CategorySerializer
