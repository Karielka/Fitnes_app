from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords # type: ignore
from django.utils import timezone

class Goal(models.Model):
    status_choices = [
        ('New', 'Новая'),
        ('In_work', 'В процессе'),
        ('Done', 'Завершена'),
        ('Failed', 'Провалена'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    description = models.CharField(max_length=255) #описание
    start_weight = models.FloatField(default=50) #начальный вес
    current_weight = models.FloatField(default=50) #текущий вес
    updated_at = models.DateTimeField(default=timezone.now) #время последнего изменения
    target_weight = models.FloatField(default=50) #желаемый вес
    start_date = models.DateField() #дата постановки цели
    end_date = models.DateField() #желаемая дата достижения цели
    status = models.CharField(max_length=20, choices=status_choices, default='Новая')
    points = models.PositiveIntegerField(default=0)  # Количество баллов за выполнение цели
    history = HistoricalRecords()  # Добавляем историю изменений

    def save(self, *args, **kwargs):
        if self.pk is not None:
            old_instance = Goal.objects.get(pk=self.pk)
            if old_instance.current_weight != self.current_weight:
                self.updated_at = timezone.now()
        super(Goal, self).save(*args, **kwargs)

class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='achievements')
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    date = models.DateField()
    points = models.PositiveIntegerField(default=1)

class UserRating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rating')
    rating = models.PositiveIntegerField(default=0)
    #функция, каждые n-единиц времени обновляющая рейтинг
    def update_rating(self):
        achievements_points_sum = self.user.achievements.aggregate(models.Sum('points'))['points__sum']
        self.rating = (achievements_points_sum or 0)
        completed_goals_points = self.user.goals.filter(status='Done').aggregate(models.Sum('points'))['points__sum']
        self.rating += (completed_goals_points or 0)
        self.save()