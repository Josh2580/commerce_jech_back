from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)  # Show the user's string representation

    class Meta:
        model = Review
        fields = ['id', 'product', 'user', 'rating', 'content', 'created_at', 'updated_at', 'reviewer_names']
        read_only_fields = ['user', 'created_at', 'updated_at']
