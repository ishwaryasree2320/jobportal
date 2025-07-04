from django.urls import path
from . import views

urlpatterns = [
    path('apply/<int:job_id>/', views.apply_job, name='apply_job'),
    path('my-applications/', views.view_applications, name='view_applications'),
    path('update-status/<int:application_id>/<str:status>/', views.update_application_status, name='update_application_status'),
]