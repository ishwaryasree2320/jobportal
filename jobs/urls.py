from django.urls import path
from .import views
from jobs.views import home
urlpatterns = [
    path('', views.home, name='home'),
     path('jobs/', views.job_list, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:pk>/', views.job_detail, name='job_detail'),
    path('jobs/post/', views.post_job, name='post_job'),
    path('jobs/manage/', views.manage_jobs, name='manage_jobs'),
    path('jobs/<int:pk>/edit/', views.edit_job, name='edit_job'),
    path('jobs/<int:pk>/delete/', views.delete_job, name='delete_job'),
    path('manage/', views.manage_posted_jobs, name='manage_jobs'), 
    path('',home),
]