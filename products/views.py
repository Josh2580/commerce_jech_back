
# products/views.py
from rest_framework import generics, permissions, serializers, filters, viewsets
from .models import Product, FeaturedProduct
from .serializers import ProductSerializer, FeaturedProductSerializer
from .permissions import IsOwnerOrReadOnly
from stores.models import Store

# List and Create Products

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    filter_backends = [filters.OrderingFilter]
    ## Ordered by date and number of sales
    ordering_fields = ['created_at', 'total_sales']  

    def get_queryset(self):
        """
        Filter products by subcategory (subcategory ID from nested router).
        """
        subcategory_id = self.kwargs.get('subcategory_pk') ## subcategory_pk from subcategory url lookup
        if subcategory_id:
            return Product.objects.filter(categories__id=subcategory_id)
        return super().get_queryset()
    
    def perform_create(self, serializer):
        user = self.request.user
        store_id = self.request.data.get('store')

        # If no store is provided in the request
        if not store_id:
            ## If User has no store and created products is 2 or above
            if not user.stores.exists() and user.products.count() >= 2:
                raise serializers.ValidationError("You must create a store to list more than 2 products.")
            ## set the first store if user has store
            store = user.stores.first()
        else:
            try:
                store = Store.objects.get(id=store_id)
            except Store.DoesNotExist:
                raise serializers.ValidationError("Store with this ID does not exist.")

        # Save the product with the store and owner
        serializer.save(store=store, owner=user)



# List all featured products
class FeaturedProductListCreateView(generics.ListCreateAPIView):
    queryset = FeaturedProduct.objects.all()
    serializer_class = FeaturedProductSerializer
    # permission_classes = [permissions.IsAdminUser]

    def perform_create(self, serializer):
        # Add extra advert logic here
        serializer.save()

# Retrieve, update, or delete a featured product
class FeaturedProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FeaturedProduct.objects.all()
    serializer_class = FeaturedProductSerializer
    # permission_classes = [permissions.IsAdminUser]

    # def get_object(self):
    #     return super().get_object()






