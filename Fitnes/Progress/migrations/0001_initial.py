# Generated by Django 5.0.4 on 2024-06-09 11:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Achievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('icon', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('points', models.PositiveIntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='achievements', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=255)),
                ('target_weight', models.FloatField()),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('status', models.CharField(choices=[('New', 'Новая'), ('In_work', 'В процессе'), ('Done', 'Завершена'), ('Failed', 'Провалена')], default='Новая', max_length=20)),
                ('points', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='goals', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
