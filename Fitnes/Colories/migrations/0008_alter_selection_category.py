# Generated by Django 5.0.4 on 2024-07-03 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Colories', '0007_delete_trainingsession'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selection',
            name='category',
            field=models.CharField(choices=[('Breakfast', 'Завтрак'), ('Dinner', 'Обед'), ('Lunch', 'Ланч'), ('Snack', 'Перекус'), ('Supper', 'Ужин')], max_length=25),
        ),
    ]
