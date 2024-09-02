# orders/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Order
from .serializers import OrderSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        order = self.get_object()
        if order.status in ['completed', 'canceled']:
            return Response({'detail': 'Cannot delete this order.'}, status=status.HTTP_400_BAD_REQUEST)
        return self.destroy(request, *args, **kwargs)
