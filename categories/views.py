from rest_framework import viewsets, filters
# from rest_framework.response import Response
from .models import Category
from products.models import Product
from .serializers import CategorySerializer

class CategoryViewset(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filterset_fields = ['parent__subcategories']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['parent']  


    def get_queryset(self):
        """
        Dynamically filter categories or subcategories based on the parent.
        """
        category_id = self.kwargs.get('category_pk')  # Root category ID from nested router
        if category_id:
            return Category.objects.filter(parent_id=category_id)  # Filter subcategories by parent
        return super().get_queryset()
