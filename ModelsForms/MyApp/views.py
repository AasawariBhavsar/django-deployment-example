from django.shortcuts import render
from MyApp.forms import UserInfoForm,UserProfileInfoForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request,'index.html')

@login_required
def special(request):
    return HttpResponse("YOU ARE LOGGED IN")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered=False
    if request.method=="POST":
        user_form=UserInfoForm(request.POST)
        user_profile_form=UserProfileInfoForm(request.POST)

        if user_form.is_valid() and user_profile_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()

            profile=user_profile_form.save(commit=False)
            profile.user=user

            if 'profile_pic' in request.FILES:
                profile.profile_pic=request.FILES['profile_pic']

            profile.save()

            registered=True
        else:

            print(user_form.errors,user_profile_form.errors)
    else:
        user_form=UserInfoForm()
        user_profile_form=UserProfileInfoForm()

    return render(request,'register.html',
    {'user_form':user_form,
    'user_profile_form':user_profile_form,
    'registered':registered
    })

def user_login(request):

    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)

        if user:
            if user.is_activate:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse('YOUR ACCOUNT IS NOT ACTIVATE')

        else:
            print('SOMEONE TRIED TO LOGIN AND FAILED')
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request,'login.html',{})


