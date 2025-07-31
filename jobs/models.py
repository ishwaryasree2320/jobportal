from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name  # ✅ correct



class Job(models.Model):
    JOB_TYPES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPES)
    category = models.ForeignKey(JobCategory, on_delete=models.SET_NULL, null=True)
    salary = models.CharField(max_length=100, blank=True)
    posted_on = models.DateTimeField(default=timezone.now)
    deadline = models.DateField()
    is_active = models.BooleanField(default=True)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='posted_jobs')
    def __str__(self):
     return f"{self.title} at {self.posted_by.employerprofile.company_name}"
