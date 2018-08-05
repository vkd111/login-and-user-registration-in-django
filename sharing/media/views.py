from django.shortcuts import render
from django.http import HttpResponse
from .forms import LoginForm
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def dashboard(request):
    return render(request,'media/dashboard.html',{'section':'dashboard'})
def user_login(request):
    if(request.method=="POST"):
        form=LoginForm(request.POST)
        if(form.is_valid()):
            cd=form.cleaned_data
            user=authenticate(username=cd['username'],password=cd['password'])
            if(user is not None):
                if(user.is_active):
                    login(request,user)
                    return HttpResponse('Authenticated Successfully')
                else:
                    return HttpResponse('Disabled Account')
            else:
                return HttpResponse('Invalid Login')
    else:
        form=LoginForm()
    return render(request,'media/login.html',{'form':form})


def register(request):
    if(request.method=='POST'):
        user_form=UserRegistrationForm(request.POST)
        if(user_form.is_valid()):
            new_user=user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request,'media/register_done.html',{'new_user':new_user})
        
    else:
        user_form=UserRegistrationForm()
    return render(request,'media/register.html',{'user_form':user_form})