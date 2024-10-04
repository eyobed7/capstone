from django.contrib import admin
from .models import User,Profile

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','bio','profile_picture')

admin.site.register(Profile, ProfileAdmin)