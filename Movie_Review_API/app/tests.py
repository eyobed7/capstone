from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model  # Import the custom user model
from .models import Review

User = get_user_model()  # Get the custom User model

def test_most_reviewed_movies_authenticated(self):
    # Log in the user and check if login is successful
    login_successful = self.client.login(username='testuser', password='testpassword')
    self.assertTrue(login_successful, "User login failed")

    # Make a GET request to the view
    response = self.client.get(reverse('most_reviewed_movies'))

    # Assert that the correct template is used for authenticated users
    self.assertTemplateUsed(response, 'most_reviewed_movies.html')

    # Assert that the response contains the most reviewed movies
    most_reviewed_movies = response.context['most_reviewed_movies']
    self.assertEqual(len(most_reviewed_movies), 2)  # There should be two movies
    self.assertEqual(most_reviewed_movies[0]['movie_title'], 'Movie 1')  # Movie 1 has more reviews


