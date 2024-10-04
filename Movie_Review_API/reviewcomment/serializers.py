from rest_framework import serializers
from .models import ReviewComment

class ReviewCommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # Access username from the user relationship
    review = serializers.CharField(source='review.movie_title', read_only=True)

    class Meta:
        model = ReviewComment
        fields = ['id', 'review', 'username', 'comment', 'created_at']
        read_only_fields = ['id', 'username', 'created_at','review']
