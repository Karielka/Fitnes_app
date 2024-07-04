from django.db import models
from django.contrib.auth.models import User
from Profiles.models import ExpertProfile
from Activity.models import Exercise
from Colories.models import Selection
        
class MasterCourse(models.Model):
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name='master_courses')
    title = models.CharField(max_length=255)
    description = models.TextField()
    duration_weeks = models.PositiveIntegerField(default=0) 
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  
    rating = models.FloatField(default=0.0)
    exercises = models.ManyToManyField(Exercise)
    selections = models.ManyToManyField(Selection)

    def update_rating(self):
        average_rating = self.reviews.aggregate(models.Avg('rating'))['rating__avg']
        if average_rating is not None:  
            self.rating = average_rating
        else:
            self.rating = None  
        self.save()

class Recommendation(models.Model):
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name='recommendations')
    course = models.ForeignKey(MasterCourse, on_delete=models.CASCADE, related_name='recommendations')
    description = models.CharField(max_length=255)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews_given')
    course = models.ForeignKey(MasterCourse, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    rating = models.FloatField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.course.update_rating()  # Вызываем метод обновления рейтинга после сохранения отзыва

class CourseSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='course_subscriptions')
    course = models.ForeignKey(MasterCourse, on_delete=models.CASCADE, related_name='subscribers')
    subscription_date = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.course.expert.update_followers_count()

#расписание индивидуальных тренировок тренера
class ExpertTimetable(models.Model):
    expert = models.ForeignKey(ExpertProfile, on_delete=models.CASCADE, related_name='expert_timetsble')
    DAYS_OF_WEEK = [
        ('Monday', 'Понедельник'),
        ('Tuesday', 'Вторник'),
        ('Wednesday', 'Среда'),
        ('Thursday', 'Четверг'),
        ('Friday', 'Пятница'),
        ('Saturday', 'Суббота'),
        ('Sunday', 'Воскресенье'),
    ]
    #с кем занятие (для раскрашивания расписания в разные цвета)
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=9, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
