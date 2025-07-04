from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)

    is_employer = models.BooleanField(default=False)
    is_job_seeker = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class EmployerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    company_name = models.CharField(max_length=100)
    company_description = models.TextField()
    company_logo = models.ImageField(upload_to='company_logos/', null=True, blank=True)
    website = models.URLField(blank=True)
    location = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.company_name} Profile"

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    skills = models.TextField()
    experience = models.CharField(max_length=100)
    education = models.TextField()
    
    def __str__(self):
        return f"{self.user.username} Profile"