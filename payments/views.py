from rest_framework import generics
from .models import PaymentMethod, UserPaymentMethod
from .serializers import PaymentMethodSerializer, UserPaymentMethodSerializer
 


class PaymentMethodListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer

class UserPaymentMethodListCreateView(generics.ListCreateAPIView):
    queryset = UserPaymentMethod.objects.all()
    serializer_class = UserPaymentMethodSerializer
    # permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]



    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class TransactionListView(generics.ListAPIView):
#     queryset = Transaction.objects.all()
#     serializer_class = TransactionSerializer
