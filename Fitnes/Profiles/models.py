from django.db import models
from django.contrib.auth.models import User

class UserCaloryProfile(models.Model):
    ACTIVITY_LEVEL_CHOICES = [
        ('sedentary', 'Sedentary (little or no exercise)'),
        ('light', 'Lightly active (light exercise/sports 1-3 days/week)'),
        ('moderate', 'Moderately active (moderate exercise/sports 3-5 days/week)'),
        ('active', 'Very active (hard exercise/sports 6-7 days a week)'),
        ('super_active', 'Super active (very hard exercise/sports & physical job)'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='calory_profile')
    birthdate = models.DateField(default='2010-01-01')
    gender = models.CharField(max_length=10)
    height = models.FloatField()  # Height in centimeters
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)

    def __str__(self):
        return f"Профиль калорий {self.user.username}"
