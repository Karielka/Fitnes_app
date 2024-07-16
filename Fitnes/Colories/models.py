from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=255)
    measurement_unit = models.CharField(max_length=20)
    calories_per_unit = models.PositiveIntegerField()
    proteins_per_unit = models.FloatField()  # белки на единицу измерения
    fats_per_unit = models.FloatField()      # жиры на единицу измерения
    carbohydrates_per_unit = models.FloatField()  # углеводы на единицу измерения

    def __str__(self):
        return self.name

class MealRecord(models.Model):
    category_choices = [('Breakfast','Завтрак'),('Dinner','Обед'),('Supper','Ужин'),('Snack','Перекус'), ('Water', 'Вода')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meal_records')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    measure = models.FloatField() # сколько граммов/милилитров было употреблено
    meal_time = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=category_choices, default='Новая')

    def __str__(self):
        return f"{self.measure} {self.product} в {self.meal_time}"

#экземпляр класса должен создаваться каждый день для каждого пользователя
#или же создаваться после циклом, для более детальной обработки калорий за день
class History(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    date = models.DateField()
    total_meals = models.PositiveIntegerField(default=0)  # количество приемов пищи за день
    total_calories = models.PositiveIntegerField(default=0)  # количество потребленных калорий за день
    total_proteins = models.FloatField(default=0)  # общее количество белков за день
    total_fats = models.FloatField(default=0)      # общее количество жиров за день
    total_carbohydrates = models.FloatField(default=0)  # общее количество углеводов за день
    #нужно дополнительное поле, которое сообщает, выполнена ли дневная норма колорий

    def update_history(self):
        # Получаем все записи MealRecord для данного пользователя и даты
        records = self.user.meal_records.filter(meal_time__date=self.date)
        self.total_meals = records.count()
        self.total_calories = records.aggregate(total_calories=models.Sum('product__calories_per_unit'))['total_calories'] or 0
        self.total_proteins = records.aggregate(total_proteins=models.Sum('product__proteins_per_unit'))['total_proteins'] or 0
        self.total_fats = records.aggregate(total_fats=models.Sum('product__fats_per_unit'))['total_fats'] or 0
        self.total_carbohydrates = records.aggregate(total_carbohydrates=models.Sum('product__carbohydrates_per_unit'))['total_carbohydrates'] or 0
        self.save()

class Selection(models.Model):
    MEAL_TIMES = [
        ('Breakfast', 'Завтрак'),
        ('Dinner', 'Обед'),
        ('Lunch', 'Ланч'),
        ('Snack', 'Перекус'),
        ('Supper', 'Ужин'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=25, choices=MEAL_TIMES)
    products = models.ManyToManyField(Product)

class TimeTable(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='time_tables')
    breakfast_time = models.TimeField(blank=True, null=True)
    lunch_time = models.TimeField(blank=True, null=True)
    dinner_time = models.TimeField(blank=True, null=True)
    go_to_sleep_time = models.TimeField(blank=True, null=True)
    #время для постоянных тренировок через TrainingSession