from django.db import models
from django.contrib.auth.models import User

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