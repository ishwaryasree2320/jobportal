from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('job', 'applicant', 'status', 'applied_date')
    list_filter = ('status', 'applied_date')
    search_fields = ('job__title', 'applicant__username')
