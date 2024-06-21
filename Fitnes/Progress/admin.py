from django.contrib import admin
from .models import Achievement, UserAchievement, UserRating

admin.site.register(Achievement)
admin.site.register(UserAchievement)
admin.site.register(UserRating)