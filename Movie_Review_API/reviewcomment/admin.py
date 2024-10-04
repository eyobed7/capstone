from django.contrib import admin
from .models import ReviewComment
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ( 'id','user','comment','review')

admin.site.register(ReviewComment, ReviewCommentAdmin)
