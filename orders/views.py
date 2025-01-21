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
    

# class OrderItemView(generics.ListCreateAPIView):
#     queryset = OrderItem.objects.all()
#     serializer_class = OrderItemSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         user = self.request.user
#         orders = Order.objects.filter(user=user)
#         order_item_reponse = []

#         for order in orders:
#             for order_item in order.items.all():  # Iterate over related OrderItem instances
#                 order_item_reponse.append(order_item)
#         return order_item_reponse
    
#     def get_cart_items(self):
#         cart = Cart.objects.get(user=self.request.user)
#         return cart.items.all()
    
#     def delete_cart(self):
#         Cart.objects.get(user=self.request.user).items.all().delete()
    

#     def perform_create(self, serializer):
#         user = self.request.user

#         try:
#             # Get the user's pending order
#             previous_order = Order.objects.get(user=user, status='pending')

#             # Retrieve cart items and add them to the previous order
#             cart_items = self.get_cart_items()
#             for cart_item in cart_items:
#                 # previous_order.items.create(
#                 #     product=cart_item.product,
#                 #     quantity=cart_item.quantity,
#                 #     price=cart_item.product.price
#                 # )
#                 self.queryset.create(
#                     order=previous_order,
#                     product=cart_item.product,
#                     quantity=cart_item.quantity,
#                     price=cart_item.product.price
#                 )

#             # Calculate the cart total and update the order
#             cart_total = sum(item.product.price * item.quantity for item in cart_items)
           
#             previous_order.total += cart_total
#             previous_order.save()
#             serializer.save(self.queryset)

#             # Clear the user's cart
#             # self.delete_cart()

#             # Use the serializer to save the order item(s)
#             # serializer = OrderSerializer(previous_order)
#             # print(f"serializer.data: {serializer.data}")
#             # return Response(serializer.data)

#         except Order.DoesNotExist:
#             raise NotFound({"message": "Create Order first before adding order Items"})

#         except Order.MultipleObjectsReturned:
#             raise ValidationError(
#                 {"message": "Multiple pending orders found. Please contact support."}
#             )


class OrderItemView(generics.ListCreateAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return all OrderItems related to the authenticated user's orders
        user = self.request.user
        orders = Order.objects.filter(user=user)
        return OrderItem.objects.filter(order__in=orders)

    def get_cart_items(self):
        # Retrieve all items in the user's cart
        cart = Cart.objects.get(user=self.request.user)
        return cart.items.all()

    def delete_cart(self):
        # Clear the user's cart
        Cart.objects.get(user=self.request.user).items.all().delete()
        # cart.items.all().delete()
        # cart.delete()

    def perform_create(self, serializer):
        user = self.request.user

        try:
            # Get the user's pending order
            previous_order = Order.objects.get(user=user, status='pending')

            # Retrieve cart items and add them to the previous order
            cart_items = self.get_cart_items()
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=previous_order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.price
                )

            # Calculate the cart total and update the order
            cart_total = sum(item.product.price * item.quantity for item in cart_items)
            previous_order.total += cart_total
            previous_order.save()

            # Clear the user's cart
            self.delete_cart()

            

        except Order.DoesNotExist:
            raise NotFound({"message": "Create Order first before adding order items"})

        except Order.MultipleObjectsReturned:
            raise ValidationError({"message": "Multiple pending orders found. Please contact support."})


    def create(self, request, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, status='pending')
        serialized_order = OrderSerializer(order)
        
        # print(f"Hoping {serialized_order.data}")
        return Response(
            {"message": "Successful", "data": serialized_order.data},  # Include serialized data in the response
            status=status.HTTP_201_CREATED,
        )
