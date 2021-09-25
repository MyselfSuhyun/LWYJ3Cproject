from django.shortcuts import render,redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,PasswordChangeForm
from .forms import CustonUserChangeForm
from django.views.decorators.http import require_http_methods,require_POST
from django.contrib.auth.decorators import login_required

@require_http_methods(['GET','POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('boards:index')
    if request.method =='POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            auth_login(request,form.get_user())
            return redirect(request.GET.get('next') or 'boards:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/login.html',context)

@require_POST
def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return redirect('boards:index')

@require_http_methods(['GET','POST'])
def signup(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request,user)
            return redirect('boards:index')
    else:
        form = UserCreationForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/signup.html',context)

@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()
    return redirect('boards:index')

@require_http_methods(['GET','POST'])
def update(request):
    if request.method =='POST':
        form = CustonUserChangeForm(request.POST,instance=request.user)
        if form.is_valid:
            form.save()
            return redirect('boards:index')
    else:
        form = CustonUserChangeForm(instance=request.user)
    context = {
        'form':form,
    }
    return render(request,'accounts/update.html',context)

@login_required
@require_http_methods(['GET','POST'])
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('boards:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {
        'form':form,
    }
    return render(request,'accounts/change_password.html',context)