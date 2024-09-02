
# products/views.py
from rest_framework import generics, permissions, serializers
from .models import Product
from .serializers import ProductSerializer
from stores.models import Store

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        user = self.request.user
        if not user.stores.exists() and Product.objects.filter(store__owner=user).count() >= 2:
            raise serializers.ValidationError("You must create a store to list more than 2 products.")
        
        store = user.stores.first()  # Assuming they must have a store if adding more than 2 products
        serializer.save(store=store)

class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
