from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta
from Colories.models import TimeTable

class TrainingSession(models.Model):
    DAYS_OF_WEEK = [
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
        ('Saturday', 'Суббота'),
        ('Sunday', 'Воскресенье'),
    ]

    time_table = models.ForeignKey(TimeTable, on_delete=models.CASCADE, related_name='training_sessions')
    day_of_week = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ('time_table', 'day_of_week', 'start_time')

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    date = models.DateField() 
    title = models.CharField(max_length=255)
    duration = models.DurationField()  
    link_to_video = models.CharField(max_length=200, default='')
    calories_burned = models.PositiveIntegerField()
    notes = models.TextField(blank=True)  

class Sleep(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sleep_records')
    date = models.DateField()
    duration = models.DurationField()  # Продолжительность сна в часах
    quality = models.CharField(max_length=20, choices=[('poor', 'Ужасный'), ('fair', 'Плохой'), ('good', 'Хороший'), ('excellent', 'Превосходный')], default='good')  # Качество сна
    calories_burned = models.PositiveIntegerField()  
    notes = models.TextField(blank=True)  

    def calculate_sleep_quality(self):
        if self.duration < timedelta(hours=3):
            self.quality = 'poor'
        elif self.duration < timedelta(hours=6):
            self.quality = 'fair'
        elif self.duration < timedelta(hours=9):
            self.quality = 'good'
        else:
            self.quality = 'excellent'

    def save(self, *args, **kwargs):
        self.calculate_sleep_quality()  # Вычисляем качество сна перед сохранением объекта
        super().save(*args, **kwargs)