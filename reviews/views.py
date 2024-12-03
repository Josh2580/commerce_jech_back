from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.exceptions import ValidationError
from .models import Review
from products.models import Product
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """
    Handles CRUD for reviews.
    """
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Associate the review with the current user
        user = self.request.user
        product_id = self.request.data.get('product')

        # Validate: Ensure user has not already reviewed this product
        if Review.objects.filter(user=user, product_id=product_id).exists():
            raise ValidationError("You have already reviewed this product.")

        product = Product.objects.get(id=product_id)
        serializer.save(user=user, product=product)
