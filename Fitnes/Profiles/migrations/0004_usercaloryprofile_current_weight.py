# Generated by Django 5.0.4 on 2024-06-16 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercaloryprofile',
            name='current_weight',
            field=models.FloatField(default=50),
        ),
    ]