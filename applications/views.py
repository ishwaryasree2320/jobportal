from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from jobs.models import Job
from .models import Application
from .forms import ApplicationForm

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
        # Employer viewing applications to their jobs
        applications = Application.objects.filter(job__company=request.user).select_related('job', 'applicant')
        template = 'applications/employer_applications.html'
    elif request.user.is_job_seeker:
        # Job seeker viewing their own applications
        applications = Application.objects.filter(applicant=request.user).select_related('job')
        template = 'applications/jobseeker_applications.html'
    else:
        return redirect('home')
    
    return render(request, template, {'applications': applications})

@login_required
def update_application_status(request, application_id, status):
    if not request.user.is_employer:
        return redirect('home')
    
    application = get_object_or_404(Application, pk=application_id, job__company=request.user)
    
    if status in [choice[0] for choice in Application.STATUS_CHOICES]:
        application.status = status
        application.save()
        messages.success(request, 'Application status updated.')
    
    return redirect('view_applications')