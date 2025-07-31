from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ['posted_by', 'company', 'posted_on']  # ✅ hide these fields
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
