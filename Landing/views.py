from django.shortcuts import redirect, render

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm #add this
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def landing_page(request):
    user = request.user
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("job_board")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    
    form = AuthenticationForm()
    return render(request=request, template_name="index.html", context={"login_form":form, "user":user})
  




# def base_page(request):
#     return render(request, 'base.html')

