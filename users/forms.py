from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, EmployerProfile, JobSeekerProfile

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    is_employer = forms.BooleanField(required=False, label='Register as Employer')
    is_job_seeker = forms.BooleanField(required=False, label='Register as Job Seeker')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'is_employer', 'is_job_seeker']

class EmployerProfileForm(forms.ModelForm):
    class Meta:
        model = EmployerProfile
        fields = ['company_name', 'company_description', 'company_logo', 'website', 'location']

class JobSeekerProfileForm(forms.ModelForm):
    class Meta:
        model = JobSeekerProfile
        fields = ['resume', 'skills', 'experience', 'education']