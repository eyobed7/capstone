# Django imports
from django.shortcuts import render, redirect, get_object_or_404  # For rendering templates and handling 404 errors
from django.contrib.auth import authenticate, login, logout, get_user_model  # For authentication functionalities
from django.urls import reverse  # For URL handling and redirection
from django.db.models import Count, Avg  # For aggregation functions (Count, Avg)
from django.contrib.auth.decorators import login_required  # For restricting access to logged-in users

# DRF (Django REST Framework) imports
from rest_framework import status, generics, filters  # Status codes, generics for CBVs, and search filtering
from rest_framework.response import Response  # For sending API responses
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated  # Permissions for API views
from rest_framework.pagination import PageNumberPagination  # Pagination functionality
from rest_framework.filters import OrderingFilter  # Filtering results based on fields
from rest_framework.decorators import api_view, permission_classes  # For function-based views with permissions
from rest_framework.exceptions import PermissionDenied  # To raise permission-related exceptions

# Third-party imports
from django_filters.rest_framework import DjangoFilterBackend  # Django filters for filtering queries

# Local app imports (models, serializers, forms)
from .models import Review  # Import the Review model
from .serializers import ReviewSerializer, UserSerializer, ReviewDetailSerializer  # Serializers for API views
from .forms import LoginForm  # Form for handling login
from .serializers import fetch_movie_details  # Custom function for fetching movie details

# Profile-related imports
from userprofile.forms import ProfileForm  # Form for handling user profiles
from userprofile.models import Profile  # User profile model

# ReviewComment-related imports
from reviewcomment.models import ReviewComment  # Model for review comments
from reviewcomment.serializers import ReviewCommentSerializer  # Serializer for review comments

User=get_user_model()

def most_reviewed_movies_view(request):
    # Query to get movie titles along with their review count and poster_url
    most_reviewed_movies = Review.objects.values('movie_title', 'poster_url').annotate(
        review_count=Count('id'),
        average_rating=Avg('rating')
    ).order_by('-review_count')  # Order by number of reviews in descending order

    # Ensure average_rating is rounded to one decimal and out of 5
    for movie in most_reviewed_movies:
        if movie['average_rating']:
            movie['average_rating'] = round(min(movie['average_rating'], 5), 1)  # Ensure it's capped at 5

    # Determine which template to render based on user's authentication status
    template = 'most_reviewed_movies.html' if request.user.is_authenticated else 'most_reviewed_movies_anonymous.html'

    return render(request, template, {'most_reviewed_movies': most_reviewed_movies})



class ReviewCommentCreateView(generics.CreateAPIView):
    serializer_class = ReviewCommentSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        # Get the 'review_id' from the URL kwargs
        review_id = self.kwargs.get('pk')

        # Retrieve the review object
        review = get_object_or_404(Review, pk=review_id)

        # Save the comment, associating it with the user and the review
        serializer.save(user=self.request.user, review=review)

class ReviewCommentListView(generics.ListAPIView):
    serializer_class = ReviewCommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the 'review_id' from the URL kwargs
        review_id = self.kwargs.get('pk')
        # Filter comments by review_id
        return ReviewComment.objects.filter(review__id=review_id)



@login_required
def update_profile(request):
    # Get the profile for the logged-in user or create one if it doesn't exist
    profile, created = Profile.objects.get_or_create(user=request.user)

    # Ensure that the current user is the owner of the profile
    if profile.user != request.user:
        raise PermissionDenied("You do not have permission to update this profile.")

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('review-list')  # Change 'review-list' to the appropriate profile view if necessary
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profileform.html', {'form': form})


@login_required
def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    reviews = user.reviews.all()  # Get all reviews submitted by this user
    context = {
        'user': user,
        'reviews': reviews,
    }
    return render(request, 'profile.html', context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_review(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user in review.liked_by.all():
        return Response({'error': 'You already liked this review'}, status=status.HTTP_400_BAD_REQUEST)

    # Add user to liked_by field
    review.liked_by.add(request.user)

    # Explicitly return only the success message
    return Response({'message': 'Review liked successfully'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unlike_review(request, pk):
    try:
        review = Review.objects.get(pk=pk)
    except Review.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.user not in review.liked_by.all():
        return Response({'error': 'You have not liked this review'}, status=status.HTTP_400_BAD_REQUEST)

    review.liked_by.remove(request.user)
    return Response({'message': 'Review unliked successfully'}, status=status.HTTP_200_OK)

class MostLikedReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        movie_title = self.kwargs['movie_title']
        # Annotate each review with the number of likes and order by like count
        return Review.objects.filter(movie_title=movie_title).annotate(like_count=Count('liked_by')).order_by('-like_count')

def my_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')  # Fetch the email
            password = form.cleaned_data.get('password')  # Fetch the password
            user = authenticate(request, email=email, password=password)  # Authenticate using email and password

            if user is not None:
                # Log the user in using session authentication
                login(request, user)

                # Get the username and pass it to the profile URL
                return redirect(reverse('profile', kwargs={'username': user.username}))  # Redirect to profile with username

            else:
                form.add_error(None, "Invalid email or password")  # Add error if authentication fails

    return render(request, 'login.html', {'loginform': form})

def my_logout(request):
    logout(request)  # Log the user out
    return redirect('my_login')



class ReviewPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# List all reviews (GET)
class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, OrderingFilter ,filters.SearchFilter]
    filterset_fields = ['movie_title', 'rating']
    ordering_fields = ['rating', 'created_at']
    ordering = ['-created_at']
    search_fields = ['movie_title','rating' ]


# Create a review (POST)
# views.py
class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated,]

    # Fetch movie data from OMDB
    def fetch_movie_data(self, movie_title):
        movie_data = fetch_movie_details(movie_title)
        if movie_data and 'Poster' in movie_data:
            return movie_data['Poster']  # Return the poster URL
        return None

    def perform_create(self, serializer, movie_title=None):
        # Fetch the movie's poster URL if the movie title is provided
        poster_url = self.fetch_movie_data(movie_title) if movie_title else None
        # Save the review with the user and poster URL (for single object creation)
        serializer.save(user=self.request.user, poster_url=poster_url)

    def perform_bulk_create(self, serializer):
        # Save multiple objects (bulk create) and fetch poster URLs for each review
        for item in serializer.validated_data:
            movie_title = item.get('movie_title')
            poster_url = self.fetch_movie_data(movie_title)
            item['poster_url'] = poster_url  # Attach poster URL
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # Handle bulk create if the request data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
            serializer.is_valid(raise_exception=True)
            self.perform_bulk_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # Handle single object creation
            movie_title = request.data.get('movie_title')  # Get the movie title from the request data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer, movie_title=movie_title)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



# Retrieve a single review by ID (GET)
class ReviewDetailView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewDetailSerializer
    permission_classes = []

# Update a review by ID (PUT/PATCH)
class ReviewUpdateView(generics.UpdateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        # Get the review instance
        instance = self.get_object()

        # Check if the request user is the creator of the review
        if instance.user != request.user:
            raise PermissionDenied("You do not have permission to update this review.")

        # Perform the regular update process
        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def handle_exception(self, exc):
        if isinstance(exc, Review.DoesNotExist):
            return Response({"detail": "Review not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)

# Delete a review by ID (DELETE)
class ReviewDeleteView(generics.DestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        # Get the review instance
        instance = self.get_object()

        # Check if the request user is the creator of the review
        if instance.user != request.user:
            return Response({"error": "You do not have permission to delete this review."}, status=status.HTTP_403_FORBIDDEN)

        # Perform the deletion
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def handle_exception(self, exc):
        if isinstance(exc, Review.DoesNotExist):
            return Response({"detail": "Review not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().handle_exception(exc)

@api_view(['POST'])
@permission_classes([])
def register_user(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # Return a success response instead of redirecting
            return Response({"message": "User is created"}, status=status.HTTP_201_CREATED)
        # Return validation errors if the serializer is not valid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
