# orders/views.py
from rest_framework import generics, permissions
from .models import Order, OrderItem
from .serializers import OrderSerializer
from cart.models import Cart, CartItem

class OrderCreateView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_cart_items(self):
        cart = Cart.objects.get(user=self.request.user)
        return cart.items.all()
    
    def delete_cart(self):
        Cart.objects.get(user=self.request.user).items.all().delete()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['items'] = [{'product': item.product, 'quantity': item.quantity, 'price': item.product.price} for item in self.get_cart_items()]
        return context

    def perform_create(self, serializer):
        user = self.request.user
        try:
            previous_order = Order.objects.get(user=user, status='pending')
            if previous_order:
                # Retrieve the cart items from self.get_cart_items()
                cart_items = self.get_cart_items()
                # Loop through the cart items and add them to the previous order's items
                for cart_item in cart_items:
                    # Create a new item in the previous order using data from the cart item
                    previous_order.items.create(
                        product=cart_item.product,
                        quantity=cart_item.quantity,
                        price=cart_item.product.price
                    )
                self.delete_cart()
                
            
        except Order.DoesNotExist:
            print("No pending orders found.")
            serializer.save(user=user)
            self.delete_cart()
        except Order.MultipleObjectsReturned:
            print("Multiple pending orders found. This should not happen!")
       

class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)



class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'order_id'
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
