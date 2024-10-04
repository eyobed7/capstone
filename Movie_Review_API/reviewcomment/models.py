from django.db import models
from app.models import Review
from app.models import User



# Create your models here.
class ReviewComment(models.Model):
    review = models.ForeignKey(Review, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)