from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import register_user,my_login
from django.urls import path
from .views import ReviewListView,my_logout,ReviewCommentListView,ReviewCommentCreateView ,ReviewCreateView,update_profile,most_reviewed_movies_view, ReviewDetailView, ReviewUpdateView, ReviewDeleteView ,like_review, unlike_review, MostLikedReviewsView ,profile_view

urlpatterns = [
    # List all reviews
    path('reviews/', ReviewListView.as_view(), name='review-list'),

    # Create a review
    path('reviews/create/', ReviewCreateView.as_view(), name='review-create'),

    # Retrieve a single review by ID
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

    # Update a review by ID
    path('reviews/<int:pk>/update/', ReviewUpdateView.as_view(), name='review-update'),

    # Delete a review by ID
    path('reviews/<int:pk>/delete/', ReviewDeleteView.as_view(), name='review-delete'),

    # register for the first time
    path('register/', register_user, name='register'),
    
    # login for the user 
    path("login",my_login,name="my_login"),

    path('reviews/<int:pk>/like/', like_review, name='like-review'),

    path('reviews/<int:pk>/unlike/', unlike_review, name='unlike-review'),

    path('reviews/most-liked/<str:movie_title>/', MostLikedReviewsView.as_view(), name='most-liked-reviews'),

    path('profile/<str:username>/', profile_view, name='profile'),

    path('profileform', update_profile, name='profileform'),
     
    # URL for listing comments related to a specific review
    path('reviews/<int:pk>/comments/', ReviewCommentListView.as_view(), name='review-comment-list'),
    
    # URL for creating a new comment for a specific review
    path('reviews/<int:pk>/comments/create/', ReviewCommentCreateView.as_view(), name='review-comment-create'),

    path('most-reviewed/', most_reviewed_movies_view, name='most_reviewed_movies'),

    path('logout/', my_logout, name='logout'),

]

