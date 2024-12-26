from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Address
from stores.models import Store
from orders.models import Order
from .serializers import AddressSerializer


class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    # permission_classes = [IsAuthenticated, IsOwnerOnly]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure the user only sees their own addresses
        return self.queryset.filter(user=self.request.user)


    def perform_create(self, serializer):
        # Automatically associate the address with the logged-in user
        serializer.save(user=self.request.user)

class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    # permission_classes = [IsAuthenticated]
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        # Ensure the user only sees their own addresses
        return self.queryset.filter(user=self.request.user)
