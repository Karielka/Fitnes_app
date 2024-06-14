from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

class Exercise(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exercises')
    date = models.DateField() 
    title = models.CharField(max_length=255)
    duration = models.DurationField()  
    # можно добавить ссылку на тренировку(например из экспертного контекста, тогда и записывать
    # количество колорий не нужно, это указано в самой тренировке)
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