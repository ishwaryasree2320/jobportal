from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, EmployerProfile, JobSeekerProfile

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_employer', 'is_job_seeker', 'is_staff')
    list_filter = ('is_employer', 'is_job_seeker', 'is_staff')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_employer', 'is_job_seeker')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

@admin.register(EmployerProfile)
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'location')
    search_fields = ('company_name', 'user__username')

@admin.register(JobSeekerProfile)
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'experience')
    search_fields = ('user__username', 'skills')

