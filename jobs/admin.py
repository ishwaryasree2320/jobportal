from django.contrib import admin
from .models import Job, JobCategory

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'posted_by', 'location', 'job_type', 'is_active')
    list_filter = ('job_type', 'is_active', 'category')
    search_fields = ('title', 'description', 'posted_by__username')  # ✅ fixed
    list_editable = ('is_active',)

@admin.register(JobCategory)
class JobCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
