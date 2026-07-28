from rest_framework import serializers
from apps.reviews.models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'text', 'rating', 'created_at']
        read_only_fields = ['user', 'created_at']
