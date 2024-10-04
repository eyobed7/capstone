from django.contrib import admin
from .models import User,Review

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'id',)

admin.site.register(User, UserAdmin)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'movie_title', 'like_count', 'rating', 'id','poster_url']  # Add the custom like_count method
    def like_count(self, obj):
        return obj.liked_by.count()  # Count the number of users who liked the review

    like_count.short_description = 'Like Count'  # Name the column in the admin panel

admin.site.register(Review,ReviewAdmin)
