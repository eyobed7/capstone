from app.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_picture', blank=True ,null=True)

    def __str__(self):
        return f"{self.user.username} - {self.bio}"