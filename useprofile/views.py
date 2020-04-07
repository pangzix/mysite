from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserLoginForm,UserRegisterForm,ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'],password=data['password'])
            if user:
                login(request,user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号密码错误")
        else:
            return HttpResponse("存在危险字符")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form }
        return render(request,'userprofie/login.html',context)
    else:
        return HttpResponse("error")

def user_logout(request):
    logout(request)
    return redirect("article:article_list")

def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            login(request,new_user)
            return  redirect("article:article_list")
        else:
            return HttpResponse("输入错误")

    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = {'form':user_register_form}
        return  render(request,'userprofie/register.html',context)
    else:
        return HttpResponse("error")

@login_required(login_url='/userprofile/login/')
def profile_edit(request,id):
    user = User.objects.get(id=id)
    profile = Profile.objects.get(user_id=id)
    if request.method == 'POST':
        if request.user != user:
            return HttpResponse("Not enough permissions")
        profile_form = ProfileForm(request.POST,request.FILES)
        if profile_form.is_valid():
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd['phone']
            profile.bio = profile_cd['bio']
            if 'avatar' in request.FILES:
                profile.avatar = profile_cd["avatar"]
            profile.save()
            return redirect("userprofile:edit",id=id)
        else:
            return HttpResponse("error")

    elif request.method == 'GET':
        profile_form = ProfileForm()
        context = {'profile_form':profile_form,'profile':profile,'user':user}
        return render(request,'userprofie/edit.html',context)
    else:
        return HttpResponse("error")

