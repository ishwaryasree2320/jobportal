from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, EmployerProfileForm, JobSeekerProfileForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Set user type
            if form.cleaned_data.get('is_employer'):
                user.is_employer = True
            elif form.cleaned_data.get('is_job_seeker'):
                user.is_job_seeker = True
            user.save()
            
            messages.success(request, 'Account created successfully! Please complete your profile.')
            return redirect('profile_complete')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile_complete(request):
    if request.user.is_employer:
        form_class = EmployerProfileForm
    elif request.user.is_job_seeker:
        form_class = JobSeekerProfileForm
    else:
        return redirect('home')
    
    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('home')
    else:
        form = form_class()
    
    return render(request, 'users/profile_complete.html', {'form': form})

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('home')
@login_required
def profile(request):
    if request.user.is_employer:
        profile = request.user.employerprofile
        template = 'users/employer_profile.html'
    elif request.user.is_job_seeker:
        profile = request.user.jobseekerprofile
        template = 'users/jobseeker_profile.html'
    else:
        return redirect('home')
    
    return render(request, template, {'profile': profile})