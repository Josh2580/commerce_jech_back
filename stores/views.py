# stores/views.py
from rest_framework import generics, permissions, serializers, viewsets
from .models import Store
from .serializers import StoreSerializer
from stores.permissions import IsOwnerOrReadOnly
from products.serializers import ProductSerializer

# class StoreListCreateView(generics.ListCreateAPIView):
#     queryset = Store.objects.all()
#     serializer_class = StoreSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def perform_create(self, serializer):
#         if self.request.user.stores.count() >= 3:  # Example condition
#             raise serializers.ValidationError("You cannot create more than 3 stores.")
#         serializer.save(owner=self.request.user)

# class StoreProductListView(generics.ListAPIView):
#     serializer_class = ProductSerializer

#     def get_queryset(self):
#         store = self.request.user.stores.get(pk=self.kwargs['store_pk'])
#         return store.products.all()

# class StoreDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Store.objects.all()
#     serializer_class = StoreSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

class StoreViewset(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    # filterset_fields = ['parent__subcategories']
    # filter_backends = [filters.OrderingFilter]
    # ordering_fields = ['parent']  