from django import forms
from .models import ExpertTimetable

class ExpertTimetableForm(forms.ModelForm):
    class Meta:
        model = ExpertTimetable
        fields = ['student', 'day_of_week', 'start_time', 'end_time']