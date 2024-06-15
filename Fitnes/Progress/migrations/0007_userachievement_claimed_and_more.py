# Generated by Django 5.0.4 on 2024-06-15 11:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Progress', '0006_remove_achievement_date_remove_achievement_user_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='userachievement',
            name='claimed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterUniqueTogether(
            name='userachievement',
            unique_together={('user', 'achievement')},
        ),
    ]