# Generated by Django 5.0.4 on 2024-06-29 20:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Expertise', '0001_initial'),
        ('Profiles', '0005_expertprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mastercourse',
            name='expert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='master_courses', to='Profiles.expertprofile'),
        ),
        migrations.AlterField(
            model_name='recommendation',
            name='expert',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to='Profiles.expertprofile'),
        ),
        migrations.CreateModel(
            name='ExpertTimetable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('Monday', 'Понедельник'), ('Tuesday', 'Вторник'), ('Wednesday', 'Среда'), ('Thursday', 'Четверг'), ('Friday', 'Пятница'), ('Saturday', 'Суббота'), ('Sunday', 'Воскресенье')], max_length=9)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('expert', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expert_timetsble', to='Profiles.expertprofile')),
            ],
        ),
        migrations.DeleteModel(
            name='ExpertProfile',
        ),
    ]
