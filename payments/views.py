from rest_framework import generics, status
from .models_methods import PaymentMethod, UserPaymentMethod
from .serializers import PaymentMethodSerializer, UserPaymentMethodSerializer, TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from orders.serializers import OrderSerializer
from rest_framework.response import Response
import requests
from orders.models import Order
import os
import logging

FLUTTERWAVE_BASE_URL = "https://api.flutterwave.com/v3"
 


class PaymentMethodListView(generics.ListAPIView):
    queryset = PaymentMethod.objects.filter(is_active=True)
    serializer_class = PaymentMethodSerializer

class UserPaymentMethodListCreateView(generics.ListCreateAPIView):
    queryset = UserPaymentMethod.objects.all()
    serializer_class = UserPaymentMethodSerializer
    permission_classes = [IsAuthenticated]



    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return transactions for the authenticated user
        return Transaction.objects.filter(user=self.request.user)

class InitializePaymentView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        amount = request.data.get('amount')
        user = request.user
        order = Order.objects.filter(status="pending", user=user).first()
        

        # order = request.data.get('order')
        if not amount:
            return Response({"error": "Amount is required"}, status=status.HTTP_400_BAD_REQUEST)
        if not order:
            return Response({"error": "There is no pending order, Add to cart and Checkout"}, status=status.HTTP_400_BAD_REQUEST)

        tx_ref = f"tx_{request.user.id}_{Transaction.objects.count() + 1}"
        data = {
            "tx_ref": tx_ref,
            "amount": amount,
            "currency": "NGN",
            "redirect_url": "http://localhost:5173/checkout/confirm-order-payment",
            "payment_options": "card",
            "customer": {
                "email": user.email,
                "phonenumber": user.profile.phone_number if hasattr(user, 'profile') else '070111222333',
                "name": f"{user.first_name} {user.last_name}",
            },
        } 

        headers = {
            "Authorization": f"Bearer {os.getenv("FLUTTERWAVE_SECRET_KEY")}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                f"{FLUTTERWAVE_BASE_URL}/payments",
                json=data,
                headers=headers,
            )

            # Inspect the response
            if response.status_code == 200:
                response_data = response.json()  # Parse JSON response
                # logging.info(f"Payment Initialize response data: {response_data}")
                # print(f"Payment Initialize response data: {response_data}")
                
                # Create a transaction
                transaction = Transaction.objects.create(
                    user=user,
                    order=order,
                    tx_ref=tx_ref,
                    amount=amount,
                    status="pending"
                )
                serializer = self.get_serializer(transaction)
                initialize_response = {"my_trx":serializer.data, "call_rsp":response_data}
                return Response(initialize_response, status=status.HTTP_201_CREATED)
            else:
                error_message = response.text  # Get raw response body
                logging.error(f"Payment failed: {error_message}")
                return Response(
                    {"error": "Payment initialization failed", "details": error_message},
                    status=response.status_code
                )
        except requests.RequestException as e:
            # Log request errors (e.g., network issues)
            logging.error(f"Request to payment API failed: {str(e)}")
            return Response({"error": "An error occurred during payment initialization"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # return Response({"error": f"Failed to initialize payment "}, status=response.status_code)


class VerifyTransactionView(generics.GenericAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        tx_ref = request.query_params.get('tx_ref')  # You can also call it transaction_id
        if not tx_ref:
            return Response({"error": "tx_ref is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            transaction = Transaction.objects.get(tx_ref=tx_ref, user=request.user)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)

        headers = {
            "Authorization": f"Bearer {os.getenv("FLUTTERWAVE_SECRET_KEY")}",
        }

        response = requests.get(
            f"{FLUTTERWAVE_BASE_URL}/transactions/verify_by_reference?tx_ref={tx_ref}",
            headers=headers,
        )

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "success" and data["data"]["status"] == "successful":
                transaction.status = "successful"
                transaction.save()
                # serialized_transaction=TransactionSerializer(transaction).data
                serialized_transaction=OrderSerializer(transaction.order).data
                return Response({"message": "Transaction verified successfully", "data": data, "order":serialized_transaction}, status=status.HTTP_200_OK)
            else:
                transaction.status = "failed"
                transaction.save()
                return Response({"error": "Transaction verification failed", "data": data}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Failed to verify transaction"}, status=response.status_code)
