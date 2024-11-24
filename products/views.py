
# products/views.py
from rest_framework import generics, permissions, serializers, viewsets,filters
from .models import Product, FeaturedProduct
from .serializers import ProductSerializer, FeaturedProductSerializer
from .permissions import IsOwnerOrReadOnly
from stores.models import Store
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

# List and Create Products

# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
#     ## Filter by Store
#     filterset_fields = ['store', 'categories']
#     ## Ordered by Popularity, time/age, price
#     ordering_fields = ['total_sales','created_at', 'price']  


#     def get_queryset(self):
#         """
#         Filter products by subcategory (subcategory ID from nested router).
#         """
#         store_id = self.kwargs.get('store_pk')  # Root category ID from nested router
#         subcategory_id = self.kwargs.get('subcategory_pk') ## subcategory_pk from subcategory url lookup
#         if subcategory_id:
#             return Product.objects.filter(categories__id=subcategory_id)
#         elif store_id:
#             return Product.objects.filter(store__id=store_id)
#         return super().get_queryset()
    
#     def perform_create(self, serializer):
#         user = self.request.user
#         store_id = self.request.data.get('store')

#         # If no store is provided in the request
#         if not store_id:
#             ## If User has no store and created products is 2 or above
#             if not user.stores.exists() and user.products.count() >= 2:
#                 raise serializers.ValidationError("You must create a store to list more than 2 products.")
#             ## set the first store if user has store
#             store = user.stores.first()
#         else:
#             try:
#                 store = Store.objects.get(id=store_id)
#             except Store.DoesNotExist:
#                 raise serializers.ValidationError("Store with this ID does not exist.")

#         # Save the product with the store and owner
#         serializer.save(store=store, owner=user)



class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing products without caching.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['categories', 'store']
    ordering_fields = ['total_sales', 'created_at', 'price']

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a product along with related data without caching.
        """
        product = self.get_object()
        similar_by_subcategories = Product.objects.filter(
            categories__in=product.categories.all()
        ).exclude(id=product.id).distinct()
        similar_by_store = Product.objects.filter(
            store=product.store
        ).exclude(id=product.id).distinct()

        return Response({
            "product": ProductSerializer(product).data,
            "similar_by_subcategories": ProductSerializer(similar_by_subcategories, many=True).data,
            "similar_by_store": ProductSerializer(similar_by_store, many=True).data,
        })
    
    
    def get_queryset(self):
        """
        Filter products by subcategory (subcategory ID from nested router).
        """
        store_id = self.kwargs.get('store_pk')  # Root category ID from nested router
        subcategory_id = self.kwargs.get('subcategory_pk') ## subcategory_pk from subcategory url lookup
        if subcategory_id:
            return Product.objects.filter(categories__id=subcategory_id)
        elif store_id:
            return Product.objects.filter(store__id=store_id)
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






