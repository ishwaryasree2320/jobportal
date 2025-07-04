from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Job, JobCategory
from .forms import JobForm
from django.core.paginator import Paginator
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

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
        return redirect('home')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobForm()
    
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def manage_jobs(request):
    if not request.user.is_employer:
        return redirect('home')
    
    jobs = Job.objects.filter(company=request.user).order_by('-posted_on')
    return render(request, 'jobs/manage_jobs.html', {'jobs': jobs})