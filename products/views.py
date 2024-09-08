
# products/views.py
from rest_framework import generics, permissions, serializers
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly
from stores.models import Store

class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        user = self.request.user
        store_id = self.request.data.get('store')

        # If no store is provided in the request
        if not store_id:
            if not user.stores.exists() and user.products.count() >= 2:
                raise serializers.ValidationError("You must create a store to list more than 2 products.")
            store = user.stores.first()
        else:
            try:
                store = Store.objects.get(id=store_id)
            except Store.DoesNotExist:
                raise serializers.ValidationError("Store with this ID does not exist.")

        # Save the product with the store and owner
        serializer.save(store=store, owner=user)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]




