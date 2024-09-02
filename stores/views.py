# stores/views.py
from rest_framework import generics, permissions, serializers
from .models import Store
from .serializers import StoreSerializer
from products.serializers import ProductSerializer

class StoreListCreateView(generics.ListCreateAPIView):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if self.request.user.stores.count() >= 3:  # Example condition
            raise serializers.ValidationError("You cannot create more than 3 stores.")
        serializer.save(owner=self.request.user)

class StoreProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        store = self.request.user.stores.get(pk=self.kwargs['store_pk'])
        return store.products.all()
