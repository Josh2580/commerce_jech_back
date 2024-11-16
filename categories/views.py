from rest_framework import viewsets
from rest_framework.response import Response
from .models import Category
from products.models import Product
from .serializers import CategorySerializer
from products.serializers import ProductSerializer


class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        """
        Dynamically filter categories or subcategories based on the parent.
        """
        category_id = self.kwargs.get('category_pk')  # Root category ID from nested router
        if category_id:
            return Category.objects.filter(parent_id=category_id)  # Filter subcategories by parent
        return super().get_queryset()




class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Filter products by subcategory (subcategory ID from nested router).
        """
        subcategory_id = self.kwargs.get('subcategory_pk')
        if subcategory_id:
            return Product.objects.filter(categories__id=subcategory_id)
        return super().get_queryset()
