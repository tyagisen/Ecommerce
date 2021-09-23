from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import User
from django.shortcuts import redirect
from django.shortcuts import render

from .forms import SignUpForm, UserProfileEdit, UserAdminProfileEdit


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, user + " You are Successfully Registered ")
    else:
        form = SignUpForm()
    return render(request, 'UserRegistration/signup.html', {'form': form})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                request.session['user_id'] = user.id
                request.session['email'] = user.email
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username or Password is Incorrect!!')
                return render(request, 'UserRegistration/login.html')
        else:
            return render(request, 'UserRegistration/login.html')
    else:
        return redirect('/dashboard/')


def user_logout(request):
    logout(request)
    return redirect('/user/login/')


def user_change_pass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)
                return redirect('/dashboard/')
            else:
                messages.info(request, '')
                return render(request, 'UserRegistration/changepass.html', {'form': fm})

        else:
            form = PasswordChangeForm(user=request.user)
            return render(request, 'UserRegistration/changepass.html', {'form': form})
    else:
        return redirect('/user/login/')


def user_profile(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            if request.user.is_superuser:
                form = UserAdminProfileEdit(request.POST, instance=request.user)
                users = User.objects.all()
                
            else:
                form = UserProfileEdit(request.POST, instance=request.user)
                users = None
            if form.is_valid():
                form.save()
                messages.success(request, "Profile Updated")
        else:
            if request.user.is_superuser:
                form = UserAdminProfileEdit(instance=request.user)
                users = User.objects.all()
            else:
                form = UserProfileEdit(instance=request.user)
                users = None
        return render(request, 'UserRegistration/profile.html',
                      {'name': request.user, 'form': form, 'users': users})
    else:
        return redirect('/user/login/')


def user_detail(request, id):
    if request.user.is_authenticated:
        fm = User.objects.get(pk=id)
        show_profile = UserAdminProfileEdit(instance=fm)
        return render(request, 'UserRegistration/userdetails.html', {'form': show_profile})
    else:
        return redirect('/user/login/')
