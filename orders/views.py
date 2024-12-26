# orders/views.py
from rest_framework import generics, permissions, status
from .models import Order, OrderItem
from rest_framework.response import Response
from .serializers import OrderSerializer, OrderItemSerializer
from cart.models import Cart
from rest_framework.exceptions import NotFound, ValidationError

class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        previous_order = Order.objects.filter(user=user, status='pending').first()
        if previous_order:
            print("There are pending orders found.")
            return Response(OrderSerializer(previous_order).data, status=status.HTTP_200_OK)
        else:
            print("No pending orders found.")
            serializer.save(user=user)


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # lookup_field = 'id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    

class OrderItemView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.filter(user=user)
        order_item_reponse = []

        for order in orders:
            for order_item in order.items.all():  # Iterate over related OrderItem instances
                order_item_reponse.append(order_item)
        return order_item_reponse
    
    def get_cart_items(self):
        cart = Cart.objects.get(user=self.request.user)
        return cart.items.all()
    
    def delete_cart(self):
        Cart.objects.get(user=self.request.user).items.all().delete()
    
    def perform_create(self, serializer):
        user = self.request.user
    
        try:
            previous_order = Order.objects.get(user=user, status='pending')
            if previous_order:
                print("previous order")
                # # Retrieve the cart items from self.get_cart_items()
                cart_items = self.get_cart_items()
                # # Loop through the cart items and add them to the previous order's items
                for cart_item in cart_items:
                #     # Create a new item in the previous order using data from the cart item
                    previous_order.items.create(
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                
                self.delete_cart()
        except Order.DoesNotExist:
            print("No order yet")
            raise NotFound({"message": "Create Order first before adding order Items"})  # Raise a 404 error
        except Order.MultipleObjectsReturned:
            print("Multiple pending orders found. This should not happen!")
            raise ValidationError(
                {"message": "Multiple pending orders found. Please contact support."}
            )
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        created_order_item = self.get_serializer().instance  # Get the created instance
        return Response(
            {"message": "Order created successfully", "order_item_id": created_order_item},
            status=status.HTTP_201_CREATED
        )


