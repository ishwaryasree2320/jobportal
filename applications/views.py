from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .models import Application
from .forms import ApplicationForm
from django.http import HttpResponseForbidden
from .models import Application
@login_required
def apply_job(request, job_id):
    if not request.user.is_job_seeker:
        return redirect('home')
    
    job = get_object_or_404(Job, pk=job_id)
    
    # Check if user already applied
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=job_id)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
         application = form.save(commit=False)
         application.job = job
         application.applicant = request.user
         application.save()
         print(f"Saved application ID: {application.id}")  # Debug
         print(f"Resume path: {application.resume.path}")  # Debug
         print(f"File exists: {os.path.exists(application.resume.path)}")
         messages.success(request, 'Your application has been submitted!')
         return redirect('job_detail', pk=job_id)
    else:
        form = ApplicationForm()
    
    context = {
        'form': form,
        'job': job,
    }
    return render(request, 'applications/apply_job.html', context)

@login_required
def view_applications(request):
    if request.user.is_employer:
        applications = Application.objects.filter(job__posted_by=request.user).select_related('job', 'applicant')
        template = 'applications/employer_applications.html'
    elif request.user.is_job_seeker:
        applications = Application.objects.filter(applicant=request.user).select_related('job')
        template = 'applications/jobseeker_applications.html'
    else:
        return redirect('home')
    
    return render(request, template, {'applications': applications})

@login_required
def update_application_status(request, application_id, new_status):
    application = get_object_or_404(Application, pk=application_id)

    # Ensure only the employer who posted the job can update it
    if application.job.posted_by != request.user:
        return HttpResponseForbidden("You don't have permission to update this application.")

    valid_statuses = ['reviewed', 'interview', 'rejected', 'hired']
    if new_status in valid_statuses:
        application.status = new_status
        application.save()

    return redirect('employer_applications')
@login_required
def employer_profile(request):
    if not request.user.is_employer:
        return redirect('home')

    # Get employer profile
    try:
        profile = request.user.employerprofile
    except:
        profile = None

    # Get jobs posted by this employer
    jobs = Job.objects.filter(posted_by=request.user)
    print(f"Found {jobs.count()} jobs for employer {request.user.username}")

    # Map each job to its applications
    job_applications = {}
    for job in jobs:
        apps = Application.objects.filter(job=job)
        print(f"Job: {job.title} - Applications: {apps.count()}")
        job_applications[job] = apps

    return render(request, 'applications/employer_profile.html', {
        'profile': profile,
        'job_applications': job_applications
    })