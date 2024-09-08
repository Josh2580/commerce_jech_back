# categories/views.py
from rest_framework import generics, permissions, viewsets
from .models import Category
from .serializers import CategorySerializer
from products.models import Product
from products.serializers import ProductSerializer
from products.permissions import IsOwnerOrReadOnly

# class CategoryCreateView(generics.CreateAPIView):
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer
#     permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]  # Example permission

# class CategoryListView(generics.ListAPIView):
#     queryset = Category.objects.filter(parent=None)  # Root categories only
#     serializer_class = CategorySerializer


# class CategoryDetailView(generics.RetrieveAPIView):
#     # queryset = Category.objects.filter(parent=None)  # Root categories only
#     queryset = Category.objects.all()
#     serializer_class = CategorySerializer



class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]  # Example permission


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


    def get_queryset(self):
        return Product.objects.filter(categories=self.kwargs['category_pk'])