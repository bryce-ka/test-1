from django.shortcuts import render, redirect, get_object_or_404
from .models import Job, Applicants, Selected
from Candidate.models import Skills
from Accounts.models import CustomUser as this_user
from .forms import NewJobForm
from django.contrib.auth.decorators import login_required
# from django.conf import settings
from django.http import HttpResponseRedirect
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.views.generic import UpdateView
# from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.conf import settings
from django.views.generic import DetailView
User = settings.AUTH_USER_MODEL

# class candidate_view(DetailView):
#     model= this_user

def rec_details(request):
    context = {
        'rec_home_page': "active",
        'rec_navbar': 1,
    }
    return render(request, 'employerdetails.html', context)


@login_required
def add_job(request):
    user = request.user
    if request.method == "POST":
        form = NewJobForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.recruiter = user
            data.save()
            return redirect('job-list')
    else:
        form = NewJobForm()
    context = {
        'add_job_page': "active",
        'form': form,
        'rec_navbar': 1,
    }
    return render(request, 'add_job.html', context)


@login_required
def edit_job(request, slug):
    user = request.user
    job = get_object_or_404(Job, slug=slug)
    if request.method == "POST":
        form = NewJobForm(request.POST, instance=job)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect('add-job-detail', slug)
    else:
        form = NewJobForm(instance=job)
    context = {
        'form': form,
        'rec_navbar': 1,
        'job': job,
    }
    return render(request, 'edit_job.html', context)


@login_required
def job_detail(request, slug):
    job = get_object_or_404(Job, slug=slug)
    context = {
        'job': job,
        'rec_navbar': 1,
    }
    return render(request, 'job_detail.html', context)


@login_required
def all_jobs(request):
    jobs = Job.objects.filter(recruiter=request.user).order_by('-date_posted')
    paginator = Paginator(jobs, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'manage_jobs_page': "active",
        'jobs': page_obj,
        'rec_navbar': 1,
    }
    return render(request, 'job_posts.html', context)


@login_required
def search_candidates(request):
    this_user_list = this_user.objects.all()
    this_users = []
    for this_user in this_user_list:
        if this_user.resume and this_user.user != request.user:
            this_users.append(this_user)

    rec1 = request.GET.get('r')
    rec2 = request.GET.get('s')

    if rec1 == None:
        li1 = this_user.objects.all()
    else:
        li1 = this_user.objects.filter(location__icontains=rec1)

    if rec2 == None:
        li2 = this_user.objects.all()
    else:
        li2 = this_user.objects.filter(looking_for__icontains=rec2)

    final = []
    this_users_final = []

    for i in li1:
        if i in li2:
            final.append(i)

    for i in final:
        if i in this_users:
            this_users_final.append(i)

    paginator = Paginator(this_users_final, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'search_candidates_page': "active",
        'rec_navbar': 1,
        'this_users': page_obj,
    }
    return render(request, 'candidate_search.html', context)


@login_required
def job_candidate_search(request, slug):
    job = get_object_or_404(Job, slug=slug)
    relevant_candidates = []
    common = []
    applicants = this_user.objects.filter(desired_time=job.job_type)
    for applicant in applicants:
        user = applicant.id
        skill_list = list(Skills.objects.filter(user=user))
        skills = []
       
    objects = zip(relevant_candidates, common)
    objects = sorted(objects, key=lambda t: t[1], reverse=True)
    objects = objects[:100]
    context = {
        'rec_navbar': 1,
        'job': job,
        'objects': objects,
        'relevant': len(relevant_candidates),

    }
    return render(request, 'job_candidate_search.html', context)


@login_required
def applicant_list(request, slug):
    job = get_object_or_404(Job, slug=slug)
    applicants = Applicants.objects.filter(job=job).order_by('date_posted')
    this_users = []
    for applicant in applicants:
        this_user = this_user.objects.filter(user=applicant.applicant).first()
        this_users.append(this_user)
    context = {
        'rec_navbar': 1,
        'this_users': this_users,

        'job': job,
    }
    return render(request, 'applicant_list.html', context)


@login_required
def selected_list(request, slug):
    job = get_object_or_404(Job, slug=slug)
    selected = Selected.objects.filter(job=job).order_by('date_posted')
    this_users = []
    for applicant in selected:
        this_user = this_user.objects.filter(user=applicant.applicant).first()
        this_users.append(this_user)
    context = {
        'rec_navbar': 1,
        'this_users': this_users,
        'job': job,
    }
    return render(request, 'selected_list.html', context)


@login_required
def select_applicant(request, can_id, job_id):
    job = get_object_or_404(Job, slug=job_id)
    this_user = get_object_or_404(this_user, slug=can_id)
    user = this_user.user
    selected, created = Selected.objects.get_or_create(job=job, applicant=user)
    applicant = Applicants.objects.filter(job=job, applicant=user).first()
    applicant.delete()
    return HttpResponseRedirect('/hiring/job/{}/applicants'.format(job.slug))


@login_required
def remove_applicant(request, can_id, job_id):
    job = get_object_or_404(Job, slug=job_id)
    this_user = get_object_or_404(this_user, slug=can_id)
    user = this_user.user
    applicant = Applicants.objects.filter(job=job, applicant=user).first()
    applicant.delete()
    return HttpResponseRedirect('/hiring/job/{}/applicants'.format(job.slug))

@login_required
def employer_home(request):
    print(request.user.is_recruiter)
    context = {
        'user': request.user,
    }
    return render(request, "employer_home.html", context)