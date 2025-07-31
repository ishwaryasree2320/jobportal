from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Job, JobCategory
from .forms import JobForm
from django.core.paginator import Paginator
from applications.models import Application
def home(request):
    jobs = Job.objects.filter(is_active=True).order_by('-posted_on')
    
    # Optional search filters
    query = request.GET.get('q')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')
    category = request.GET.get('category')
    
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(company__employerprofile__company_name__icontains=query)
        )
    if location:
        jobs = jobs.filter(location__icontains=location)
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    if category:
        jobs = jobs.filter(category__id=category)
    
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = JobCategory.objects.all()

    context = {
        'jobs': page_obj,
        'categories': categories,
        'search_query': query or '',
    }
    return render(request, 'jobs/job_list.html', context)


def job_list(request):
    jobs = Job.objects.filter(is_active=True).order_by('-posted_on')
    # Search functionality
    query = request.GET.get('q')
    location = request.GET.get('location')
    job_type = request.GET.get('job_type')
    category = request.GET.get('category')
    
    if query:
        jobs = jobs.filter(
            Q(title__icontains=query) | 
            Q(description__icontains=query) |
            Q(company__employerprofile__company_name__icontains=query)
        )
    
    if location:
        jobs = jobs.filter(location__icontains=location)
    
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    if category:
        jobs = jobs.filter(category__id=category)
    
    # Pagination
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = JobCategory.objects.all()
    
    context = {
        'jobs': page_obj,
        'categories': categories,
        'search_query': query or '',
    }
    return render(request, 'jobs/job_list.html', context)

@login_required
def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk)
    has_applied = False

    if request.user.is_job_seeker:
        has_applied = job.application_set.filter(applicant=request.user).exists()

    # Get similar jobs (same category, different job)
    similar_jobs = Job.objects.filter(category=job.category).exclude(pk=job.pk)[:5]

    context = {
        'job': job,
        'has_applied': has_applied,
        'similar_jobs': similar_jobs,
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
def post_job(request):
    if not request.user.is_employer:
        messages.error(request, "Only employers can post jobs.")
        return redirect('home')

    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.company = request.user  # ✅ Set the company before saving
            job.save()
            messages.success(request, "Job posted successfully!")
            return redirect('employer_profile')  # redirect after successful post
    else:
        form = JobForm()

    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def manage_jobs(request):
    user = request.user  # already present

    # 🔽 ADD THESE DEBUG PRINTS BELOW
    print(f"Current user: {request.user}")
    print("Jobs posted by this user:")
    for job in Job.objects.filter(posted_by=request.user):
        print(f" - {job.title} (ID: {job.id})")

    jobs = Job.objects.filter(posted_by=user)
    applications = {}

    for job in jobs:
        job_applications = Application.objects.filter(job=job)
        applications[job.id] = job_applications

    return render(request, 'jobs/manage_jobs.html', {'jobs': jobs, 'applications': applications
    })

@login_required
def edit_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user)

    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('manage_jobs')
    else:
        form = JobForm(instance=job)

    return render(request, 'jobs/edit_job.html', {'form': form, 'job':job})



@login_required
def delete_job(request, pk):
    job = get_object_or_404(Job, pk=pk, company=request.user)
    job.delete()
    messages.success(request, 'Job deleted successfully!')
    return redirect('manage_jobs')

@login_required
def manage_posted_jobs(request):
    jobs = Job.objects.filter(posted_by=request.user)  # Only jobs posted by current employer


    job_applicants = {}
    for job in jobs:
        applicants = Application.objects.filter(job=job)
        job_applicants[job.id] = applicants

    context = {
        'jobs': jobs,
        'job_applications': job_applicants,
    }
    return render(request, 'jobs/manage_jobs.html', context)
