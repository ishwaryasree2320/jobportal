from django.urls import path
from . import views

urlpatterns = [
    path('employer/', views.employer_profile, name='employer_profile'),
    path('jobseeker/', views.view_applications, name='jobseeker_applications'),
    path('<int:application_id>/status/<str:new_status>/', views.update_application_status, name='update_application_status'),
]
