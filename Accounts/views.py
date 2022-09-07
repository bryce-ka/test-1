# from email import message
from ast import Return
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import CandidateFormNew, RecruiterFormNew
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.generic import RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from Accounts.admin import UserChangeForm
from Accounts.models import CustomUser as Profile
from Candidate.models import Skills 
from Candidate.forms import NewSkillForm
from django.utils.translation import gettext, gettext_lazy as lazy

def passwordsChangeView(PasswordChangeView):
    form_class = PasswordChangeView
    success_url = "/login/"


@login_required
def redirect_account(request):
    if request:
        this_user = request.user
        role = this_user.is_recruiter   
        if role:
            print("company")
            return redirect('/company/home')
        else:
            print("candidate")
            return redirect('/candidate/home')
    else:
        return redirect('/landing/')


def register_user(request):

    context = {
    'recruiterForm' :RecruiterFormNew,
    'candidateForm' : CandidateFormNew,
    }

    if request.method == "POST":
        if 'candidate' in request.POST:
            form = CandidateFormNew(request.POST, request.FILES, initial={'is_candidate': True})
            if form.is_valid():
                user = form.save()
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/login/")
                else:
                    messages.error(request, 'Username or password is incorrect!')
            else:
                form = CandidateFormNew(initial={'is_candidate': True})

        elif 'company' in request.POST:
            form = RecruiterFormNew(request.POST, initial={'is_employer': True})
            if form.is_valid():
                user = form.save()
                if user is not None:
                    login(request, user)
                    return HttpResponseRedirect("/login/")
                else:
                    messages.error(request, 'Username or password is incorrect!')
            else:
                form =RecruiterFormNew(initial={'is_employer': True})

            
    return render(request, 'registration/register.html', context = context)  

  

# @login_required()
# def logout_view(request):



@login_required
def my_profile(request):
    pass


@login_required
def edit_profile(request):
    
    this_profile = Profile.objects.filter(email = request.user).first()
    print(this_profile)
    form = UserChangeForm(request.POST, request.FILES, instance=this_profile)
    if request.method == 'POST':
        form = UserChangeForm(request.POST, request.FILES, instance=this_profile)
        print(form)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = this_profile
            data.save()
            return redirect('my-profile')
    else:
        form = UserChangeForm(instance=this_profile)
    context = {
        'form': form,
    }
    return render(request, 'edit_profile.html', context)


@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    you = p.user
    user_skills = Skills.objects.filter(user=you)
    context = {
        'u': you,
        'profile': p,
        'skills': user_skills,
    }
    return render(request, 'profile.html', context)

@login_required
def profile(request):
    return render(request, 'accounts/profile.html', {'title': lazy('Profile'), 'pretitle': lazy('Manage your profile')})

@login_required
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return HttpResponseRedirect("/login/")
    return render(request, 'registration/logout.html')

def login_view(request):

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return HttpResponseRedirect("/account/redirect/")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="registration/login.html", context={"login_form":form})  
