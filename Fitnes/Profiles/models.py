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

    GOAL_CHOICES = [
        ('lose', 'Lose weight'),
        ('gain', 'Gain weight'),
        ('maintain', 'Maintain weight'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='calory_profile')
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)
    height = models.FloatField()  # Height in centimeters
    weight = models.FloatField()  # Weight in kilograms #start_weight
    #current_weight = models.FloatField()  # Weight in kilograms
    target_weight = models.FloatField()  # Weight in kilograms
    goal = models.CharField(max_length=10, choices=GOAL_CHOICES)
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)
    target_date = models.DateField()  # Date to reach the goal

    def __str__(self):
        return f"{self.user.username}'s Calory Profile"
