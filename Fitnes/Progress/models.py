from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords # type: ignore
from django.utils import timezone
from Profiles.models import UserCaloryProfile
from datetime import timedelta

class WeightHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_history')
    weight = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

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
    status = models.CharField(max_length=20, choices=status_choices, default='New')
    points = models.PositiveIntegerField(default=0)  # Количество баллов за выполнение цели
    history = HistoricalRecords()  # Добавляем историю изменений

    def save(self, *args, **kwargs):
        if self.pk is None:  # Проверка при создании новой цели
            active_goals = Goal.objects.filter(user=self.user, status__in=['New', 'In_work'])
            if active_goals.exists():
                raise ValueError("У вас уже есть активная цель. Завершите текущую цель, прежде чем создавать новую.")
        
        if self.pk is not None:
            old_instance = Goal.objects.get(pk=self.pk)
            if old_instance.current_weight != self.current_weight:
                self.updated_at = timezone.now()
                WeightHistory.objects.create(user=self.user, weight=self.current_weight)  # Добавляем запись в историю
                Prof = UserCaloryProfile.objects.get(user=self.user)
                Prof.current_weight = self.current_weight
                Prof.save()
        super(Goal, self).save(*args, **kwargs)
    
    def update_status_by_time(self):
        if self.status == 'New' and timezone.now().date() >= self.start_date + timedelta(days=1):
            self.status = 'In_work'
            self.save()
        elif ((self.status == 'In_work') or (self.status == 'New')) and self.current_weight <= self.target_weight:
            self.status = 'Done'
            self.save()

class Achievement(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)
    points = models.PositiveIntegerField(default=1)
    rule = models.TextField(default='', help_text='''Запрос на питоне для определения выполнения задания
    Будем считать, что оно возращает кортеж из двух объектов. Текущего количества условных единиц и необходимого''')
    needed_for_reach = models.PositiveIntegerField(default=1)

class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    date_earned = models.DateField(auto_now_add=True)
    completed = models.BooleanField(default=False) # завершено
    claimed = models.BooleanField(default=False)  # собрано

    class Meta:
        unique_together = ('user', 'achievement')

class UserRating(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rating')
    rating = models.PositiveIntegerField(default=0)

    def update_rating(self):
        achievements_points_sum = UserAchievement.objects.filter(user=self.user).aggregate(models.Sum('achievement__points'))['achievement__points__sum'] or 0
        completed_goals_points = self.user.goals.filter(status='Done').aggregate(models.Sum('points'))['points__sum'] or 0
        self.rating = achievements_points_sum + completed_goals_points
        self.save()
        GlobalRating.update_user_rating(self.user.id, self.rating)

class GlobalRating(models.Model):
    ratings = models.JSONField(default=dict)

    @classmethod
    def update_user_rating(cls, user_id, new_rating):
        rating_record, created = cls.objects.get_or_create(pk=1)
        rating_record.ratings[str(user_id)] = new_rating
        rating_record.save()

    @classmethod
    def get_user_rank(cls, user_id):
        rating_record = cls.objects.get(pk=1)
        sorted_ratings = sorted(rating_record.ratings.items(), key=lambda x: x[1], reverse=True)
        for rank, (uid, rating) in enumerate(sorted_ratings, 1):
            if str(user_id) == uid:
                return rank
        return None