# colories/forms.py
from django import forms
from .models import Sleep
from datetime import timedelta

class SleepRecordFormForCreate(forms.ModelForm):
    hours = forms.IntegerField(min_value=0, max_value=23, label="Hours", required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    minutes = forms.IntegerField(min_value=0, max_value=59, label="Minutes", required=True, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Sleep
        fields = ['date', 'notes']
        widgets = {
            'notes': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        hours = cleaned_data.get('hours')
        minutes = cleaned_data.get('minutes')

        if hours is not None and minutes is not None:
            duration = timedelta(hours=hours, minutes=minutes)
            cleaned_data['duration'] = duration

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.duration = self.cleaned_data['duration']
        if commit:
            instance.save()
        return instance
