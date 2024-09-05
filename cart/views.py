# cart/views.py
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from products.models import Product

class CartRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = CartSerializer
    queryset = Cart.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self):
        auth_user = self.request.user.is_authenticated
        user = self.request.user    
        session_key = self.request.session.session_key or self.request.session.create()

        


        if auth_user:
            try:
                session_cart = Cart.objects.filter(session_key=session_key).first()
                user_cart = Cart.objects.get_or_create(user=user)[0]

                # Return the cart's ID or any other detail you'd like to return
                if session_cart:
                    # Assign items from session_cart to user_cart
                    user_cart.items.set(session_cart.items.all())  # Use the set() method

                    # Optional: Delete the session cart if needed after merging
                    session_cart.delete()

                    return user_cart  # Return the updated user_cart
                elif user_cart:
                    return user_cart
                else:
                    # Handle case where neither cart is found
                    return Response({"detail": "Cart not found."}, status=404)
            except Cart.DoesNotExist:
                return Response({"detail": "Cart not found."}, status=404)
 

        # session_key = self.request.session.session_key or self.request.session.create()
        return Cart.objects.get_or_create(session_key=session_key)[0]

    


class CartItemCreateUpdateDeleteView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_cart(self):
        if self.request.user.is_authenticated:
            return Cart.objects.get_or_create(user=self.request.user)[0]
        session_key = self.request.session.session_key or self.request.session.create()
        return Cart.objects.get_or_create(session_key=session_key)[0]

    def perform_create(self, serializer):
        cart = self.get_cart()
        product_id = self.request.data.get('product')
        quantity = self.request.data.get('quantity')
        # print(quantity)
        product = Product.objects.get(id=product_id)
        existing_item = CartItem.objects.filter(cart=cart, product=product).first()
        # print(existing_item)
        
        if existing_item:
            # Update the quantity if the item already exists in the cart
            qty = existing_item.quantity + int(quantity)
            existing_item.quantity = qty
            existing_item.save()  # Save the updated CartItem
            serializer = CartItemSerializer(existing_item)  # Serialize the updated CartItem
            
        else:
            serializer.save(cart=cart)

    # def perform_update(self, serializer):
    #     cart = self.get_cart()
    #     product_id = self.request.data.get('product')
    #     product = Product.objects.get(id=product_id)
    #     cart_item = CartItem.objects.get(cart=cart, product=product)
    #     serializer.save(cart=cart_item.cart)

    # def perform_destroy(self, instance):
    #     instance.delete()

class CartItemUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CartItemSerializer
    queryset = CartItem.objects.all()
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_cart(self):
        if self.request.user.is_authenticated:
            return Cart.objects.get_or_create(user=self.request.user)[0]
        session_key = self.request.session.session_key or self.request.session.create()
        return Cart.objects.get_or_create(session_key=session_key)[0]


    def perform_update(self, serializer):
        cart = self.get_cart()
        product_id = self.request.data.get('product')
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.get(cart=cart, product=product)
        serializer.save(cart=cart_item.cart)

    def perform_destroy(self, instance):
        instance.delete()
