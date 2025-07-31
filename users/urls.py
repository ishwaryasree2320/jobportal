from django.urls import path
from . import views
from .views import employer_profile
urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/complete/', views.profile_complete, name='profile_complete'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('employer/profile/', employer_profile, name='employer_profile'),
    

]
