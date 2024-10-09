from django.urls import path
from .views import register_user,my_login
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

    # to like a movie based on the review id
    path('reviews/<int:pk>/like/', like_review, name='like-review'),

    # To unlike a movie based on the review id
    path('reviews/<int:pk>/unlike/', unlike_review, name='unlike-review'),

    # To see the likes of a movie
    path('reviews/likes/<str:movie_title>/', MostLikedReviewsView.as_view(), name='most-liked-reviews'),

    # To see profile
    path('profile/<str:username>/', profile_view, name='profile'),

    #To create profile or update the existing one
    path('profileform', update_profile, name='profileform'),

    # URL for listing comments related to a specific review
    path('reviews/<int:pk>/comments/', ReviewCommentListView.as_view(), name='review-comment-list'),

    # URL for creating a new comment for a specific review
    path('reviews/<int:pk>/comments/create/', ReviewCommentCreateView.as_view(), name='review-comment-create'),

    # URL for to see the website
    path('', most_reviewed_movies_view, name='most_reviewed_movies'),

    # URL for logout the user
    path('logout/', my_logout, name='logout'),

]



