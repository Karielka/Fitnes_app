# Generated by Django 5.0.4 on 2024-06-12 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profiles', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercaloryprofile',
            name='age',
        ),
        migrations.RemoveField(
            model_name='usercaloryprofile',
            name='goal',
        ),
        migrations.RemoveField(
            model_name='usercaloryprofile',
            name='target_date',
        ),
        migrations.RemoveField(
            model_name='usercaloryprofile',
            name='target_weight',
        ),
        migrations.RemoveField(
            model_name='usercaloryprofile',
            name='weight',
        ),
        migrations.AddField(
            model_name='usercaloryprofile',
            name='birthdate',
            field=models.DateField(default='2010-01-01'),
        ),
    ]
