from datetime import date
from django.db import models
from django.contrib.auth.models import User

class ExpertProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='expert_profile')
    nickname = models.CharField(max_length=20)
    experience_years = models.PositiveIntegerField(default=0)  
    price_per_hour = models.PositiveIntegerField(default=0)  
    followers_count = models.PositiveIntegerField(default=0)

    def update_followers_count(self):
        # Используем строковую ссылку для CourseSubscription
        from Expertise.models import CourseSubscription
        self.followers_count = CourseSubscription.objects.filter(course__expert=self).count()
        self.save()

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
    current_weight = models.FloatField(default=50)  # Текущий вес
    activity_level = models.CharField(max_length=20, choices=ACTIVITY_LEVEL_CHOICES)

    def __str__(self):
        return f"Профиль калорий {self.user.username}"

    @property
    def daily_calorie_needs(self):
        age = date.today().year - self.birthdate.year
        if self.gender.lower() == 'male':
            need = 10 * self.current_weight + (6.25 * self.height) - (5 * age) + 5
        else:
            need = 10 * self.current_weight + (6.25 * self.height) - (5 * age) - 161
        return need

    @classmethod
    def per_day_calories(cls, user_name):
        profile = cls.objects.get(user__username=user_name)
        return profile.daily_calorie_needs


class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('user', 'User'),
        ('expert', 'Expert'),
        ('admin', 'Admin'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    #avatar = models.ImageField(null=True, blank=True, upload_to="avatars/", default='avatars/default.png')
    rating = models.IntegerField(default=0)
    type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    
    def get_user_type(self):
        return self.type

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


class ProfileManager(models.Manager):
    def get_by_type(self, user_type):
        return self.filter(type=user_type)