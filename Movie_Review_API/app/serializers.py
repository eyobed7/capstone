# Django REST Framework (DRF) imports
from rest_framework import serializers  # Import base serializer functionalities from DRF

# Local models and user model import
from .models import Review  # Import the Review model to be serialized
from django.contrib.auth import get_user_model  # Use get_user_model in case of custom user model

# Import nested serializers
from reviewcomment.serializers import ReviewCommentSerializer  # Serializer for handling ReviewComment objects


# Import the requests library
import requests  # Allows making HTTP requests to interact with external APIs


User=get_user_model()

class ReviewSerializer(serializers.ModelSerializer):
    comments = ReviewCommentSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)  # Access username from the user relationship
    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'username','poster_url','comments']
        read_only_fields = ['username','comments','poster_url']

    def get_movie_details(self, obj):
        # Fetch movie details from OMDb using the movie title from the review
        return fetch_movie_details(obj.movie_title)

    def validate_rating(self, value):
        """
        Ensure the rating is between 1 and 5.
        """
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        """
        Ensure that movie_title and review_content are provided.
        """
        if not data.get('movie_title'):
            raise serializers.ValidationError("Movie Title is required.")
        if not data.get('review_content'):
            raise serializers.ValidationError("Review Content is required.")
        return data

class ReviewDetailSerializer(serializers.ModelSerializer):
    comments = ReviewCommentSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)  # Access username from the user relationship
    movie_details = serializers.SerializerMethodField()  # Custom field for movie details
    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'username','movie_details','poster_url','comments']
        read_only_fields = ['username','comments','poster_url']

    def get_movie_details(self, obj):
        # Fetch movie details from OMDb using the movie title from the review
        return fetch_movie_details(obj.movie_title)


def fetch_movie_details(movie_title):
    api_key = '77f03f24'  # OMDb API key
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey={api_key}'

    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()  # Return the movie details as a dictionary
        else:
            return {'error': 'Movie not found'}
    except requests.RequestException:
        return {'error': 'Failed to connect to OMDb'}

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])  # Set hashed password
        user.save()
        return user


class LikeReviewSerializer(serializers.ModelSerializer):
    total_likes = serializers.IntegerField(source='total_likes', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'total_likes']
