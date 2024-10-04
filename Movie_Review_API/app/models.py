from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        """
        Create and return a regular user with an email, username, and password.
        """
        if not email:
            raise ValueError("The Email field is required")
        if not username:
            raise ValueError("The Username field is required")

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        """
        Create and return a superuser with email, username, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, max_length=255)
    username = models.CharField(unique=True, max_length=255)  # Set unique=True
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']  # Require username for creation

    def __str__(self):
        return self.username

from django.contrib.auth import get_user_model

User = get_user_model()

class Review(models.Model):
    movie_title = models.CharField(max_length=255)
    review_content = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE ,related_name='reviews')
    created_at = models.DateTimeField(auto_now_add=True)
    poster_url = models.URLField(max_length=500, null=True, blank=True)  # Add this field for the image URL

    # Track likes with a Many-to-Many relationship
    liked_by = models.ManyToManyField(User, related_name='liked_reviews', blank=True)

    def clean(self):
        if not self.movie_title:
            raise ValidationError('Movie Title is required.')
        if not self.review_content:
            raise ValidationError('Review Content is required.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Validate before saving
        super().save(*args, **kwargs)

    def total_likes(self):
        return self.liked_by.count()
    


    def __str__(self):
        return f"{self.movie_title} - {self.user.username}"
    
