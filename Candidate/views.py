from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Accounts.models import CustomUser as Profile
# Create your views here.

from django.shortcuts import render, redirect, get_object_or_404
from .models import Skills, AppliedJobs, SavedJobs
from Company.models import Job, Applicants, Selected
from django.contrib.auth.decorators import login_required
# from django.conf import settings
from django.http import HttpResponseRedirect
from Accounts.admin import UserChangeForm
# from django.contrib import messages
# from django.views.generic import UpdateView
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from job_board.filters import OrderFilter

def home(request):
    context = {
        'home_page': "active",
    }
    return render(request, 'cand_home.html', context)

def job_search_list(request):

    query = request.GET.get('p')
    
    jobs = Job.objects.all()

    searchFilter = OrderFilter(request.GET, queryset= jobs )
    jobs = searchFilter.qs     
    final_list = []
    for i in jobs:
        
        final_list.append(i)
    paginator = Paginator(final_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'jobs': page_obj,
        'query': query,
        'filter': searchFilter
    }
    return render(request, 'job_search_list.html', context)


@login_required
def job_detail(request, slug):
    if request.user.is_authenticated:
        job = get_object_or_404(Job, slug=slug)
        apply_button = 0
        save_button = 0

        profile = Profile.objects.filter(email = request.user).first()

        if AppliedJobs.objects.filter(user=profile).filter(job=job).exists():
            apply_button = 1
        if SavedJobs.objects.filter(user=profile).filter(job=job).exists():
            save_button = 1
        relevant_jobs = []
        jobs1 = Job.objects.filter(
            company__icontains=job.company).order_by('-date_posted')
        jobs2 = Job.objects.filter(
            job_type__icontains=job.job_type).order_by('-date_posted')
        jobs3 = Job.objects.filter(
            title__icontains=job.title).order_by('-date_posted')
        for i in jobs1:
            if len(relevant_jobs) > 5:
                break
            if i not in relevant_jobs and i != job:
                relevant_jobs.append(i)
        for i in jobs2:
            if len(relevant_jobs) > 5:
                break
            if i not in relevant_jobs and i != job:
                relevant_jobs.append(i)
        for i in jobs3:
            if len(relevant_jobs) > 5:
                break
            if i not in relevant_jobs and i != job:
                relevant_jobs.append(i)
        return render(request, 'c_job_detail.html', {'job': job, 'apply_button': apply_button, 'save_button': save_button, 'relevant_jobs': relevant_jobs, 'candidate_navbar': 1})

        #return render(request, 'c_job_detail.html', {'job': job, 'profile': profile, 'apply_button': apply_button, 'save_button': save_button, 'relevant_jobs': relevant_jobs, 'candidate_navbar': 1})
    else:
        print("User is not logged in :(")
        job = get_object_or_404(Job, slug=slug)
        apply_button = 0
        save_button = 0
        relevant_jobs = []
        jobs1 = Job.objects.filter(
            company__icontains=job.company).order_by('-date_posted')
        jobs2 = Job.objects.filter(
            job_type__icontains=job.job_type).order_by('-date_posted')
        jobs3 = Job.objects.filter(
            title__icontains=job.title).order_by('-date_posted')
        for i in jobs1:
            if len(relevant_jobs) > 5:
                break
            if i not in relevant_jobs and i != job:
                relevant_jobs.append(i)
        for i in jobs2:
            if len(relevant_jobs) > 5:
                break
            if i not in relevant_jobs and i != job:
                relevant_jobs.append(i)
        for i in jobs3:
            if len(relevant_jobs) > 5:
                break
            if i not in relevant_jobs and i != job:
                relevant_jobs.append(i)
    if job.cloud or job.languages or job.property_type:
        pe = 1
        return render(request, 'c_job_detail_copy.html', {'job': job, 'apply_button': apply_button, 'save_button': save_button, 'relevant_jobs': relevant_jobs, 'candidate_navbar': 1,'pe':pe })
    else:
         return render(request, 'c_job_detail_copy.html', {'job': job, 'apply_button': apply_button, 'save_button': save_button, 'relevant_jobs': relevant_jobs, 'candidate_navbar': 1,'pe':pe })
  


@login_required
def saved_jobs(request):
    jobs = SavedJobs.objects.filter(
        user=request.user).order_by('-date_posted')
    return render(request, 'saved_jobs.html', {'jobs': jobs, 'candidate_navbar': 1})


@login_required
def applied_jobs(request):
    jobs = AppliedJobs.objects.filter(
        user=request.user).order_by('-date_posted')
    statuses = []
    for job in jobs:
        if Selected.objects.filter(job=job.job).filter(applicant=request.user).exists():
            statuses.append(0)
        elif Applicants.objects.filter(job=job.job).filter(applicant=request.user).exists():
            statuses.append(1)
        else:
            statuses.append(2)
    zipped = zip(jobs, statuses)
    return render(request, 'applied_jobs.html', {'zipped': zipped, 'candidate_navbar': 1})


@login_required
def intelligent_search(request):
    relevant_jobs = []
    common = []
    job_skills = []
    user = request.user
    profile = Profile.objects.filter(user=user).first()
    my_skill_query = Skills.objects.filter(user=user)
    my_skills = []
    for i in my_skill_query:
        my_skills.append(i.skill.lower())
    if profile:
        jobs = Job.objects.filter(
            job_type=profile.looking_for).order_by('-date_posted')
    else:
        jobs = Job.objects.all()
    for job in jobs:
        skills = []
        sk = str(job.skills_req).split(",")
        for i in sk:
            skills.append(i.strip().lower())
        common_skills = list(set(my_skills) & set(skills))
        if (len(common_skills) != 0 and len(common_skills) >= len(skills)//2):
            relevant_jobs.append(job)
            common.append(len(common_skills))
            job_skills.append(len(skills))
    objects = zip(relevant_jobs, common, job_skills)
    objects = sorted(objects, key=lambda t: t[1]/t[2], reverse=True)
    objects = objects[:100]
    context = {
        'intel_page': "active",
        'jobs': objects,
        'counter': len(relevant_jobs),
    }
    return render(request, 'intelligent_search.html', context)





def candidate_details(request):
    return render(request, 'details.html')


@login_required
@csrf_exempt
def delete_skill(request, pk=None):
    if request.method == 'POST':
        id_list = request.POST.getlist('choices')
        for skill_id in id_list:
            Skills.objects.get(id=skill_id).delete()
        return redirect('my-profile')


@login_required
def save_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    saved, created = SavedJobs.objects.get_or_create(job=job, user=user)
    return HttpResponseRedirect('/candidate/job/{}'.format(job.slug))


@login_required
def apply_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    applied, created = AppliedJobs.objects.get_or_create(job=job, user=user)
    applicant, creation = Applicants.objects.get_or_create(
        job=job, applicant=user)
    return HttpResponseRedirect('/job/{}'.format(job.slug))


@login_required
def remove_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    saved_job = SavedJobs.objects.filter(job=job, user=user).first()
    saved_job.delete()
    return HttpResponseRedirect('/candidate/job/{}'.format(job.slug))

@login_required
def edit_profile(request):
    you = request.user
    profile = Profile.objects.filter(email = request.user).first()
    if request.method == 'POST':
        form = UserChangeForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = you
            data.save()
            return redirect('my-profile')
    else:
        form = UserChangeForm(instance=profile)
    context = {
        'form': form,
    }
    return render(request, 'edit_profile.html', context)

@login_required
def my_profile(request):
    you = request.user
    profile = Profile.objects.filter(email = request.user).first()
    
    context = {
        'u': you,
        'profile': profile,
        'profile_page': "active",
    }
    return render(request, 'profile.html', context)

@login_required
def profile_view(request, slug):
    
    you = Profile.objects.filter(email = request.user).first()
   
    context = {
        'u': you,


    }
    return render(request, 'profile.html', context)
