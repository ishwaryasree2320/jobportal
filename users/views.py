from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, EmployerProfileForm, JobSeekerProfileForm
from applications.models import Application
from jobs.models import Job
from .models import EmployerProfile
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
    user = request.user

    if user.is_employer:
        try:
            profile = user.employerprofile
        except:
            return redirect('profile_complete')  # Ask them to fill profile if not exists
        template = 'users/employer_profile.html'

    elif user.is_job_seeker:
        try:
            profile = user.jobseekerprofile
        except:
            return redirect('profile_complete')
        template = 'users/jobseeker_profile.html'
    
    else:
        return redirect('home')

    return render(request, template, {'profile': profile})
@login_required
def edit_profile(request):
    user = request.user

    if user.is_employer:
        profile = user.employerprofile
        form_class = EmployerProfileForm
    elif user.is_job_seeker:
        profile = user.jobseekerprofile
        form_class = JobSeekerProfileForm
    else:
        return redirect('home')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
    else:
        form = form_class(instance=profile)

    return render(request, 'users/edit_profile.html', {'form': form})
from collections import defaultdict
@login_required
def employer_profile(request):
    user = request.user
    try:
        profile = EmployerProfile.objects.get(user=user)
    except EmployerProfile.DoesNotExist:
        profile = None

    jobs = Job.objects.filter(company=user)

    jobs_with_applications = []

    for job in jobs:
        applications = Application.objects.filter(job=job).select_related('applicant')
        jobs_with_applications.append({
            'job': job,
            'applications': applications
        })

    return render(request, 'users/employer_profile.html', {
        'profile': profile,
        'jobs_with_applications': jobs_with_applications
    })


@login_required
def manage_posted_jobs(request):
    user = request.user
    if not user.is_employer:
        return redirect('home')

    try:
        employer_profile = user.employerprofile
    except EmployerProfile.DoesNotExist:
        return redirect('profile_complete')

    jobs = Job.objects.filter(company=user)
    job_applications = {}

    for job in jobs:
        applications = Application.objects.filter(job=job).select_related('applicant')
        job_applications[job] = applications

    return render(request, 'jobs/manage_jobs.html', {
        'jobs': jobs,
        'job_applications': job_applications,
    })

