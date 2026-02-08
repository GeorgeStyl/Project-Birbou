from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group, User 
from .forms import ExtendedSignupForm 

def signup_view(request):
    if request.method == "POST":
        form = ExtendedSignupForm(request.POST) 
        role = request.POST.get("role")
        
        if form.is_valid() and role in ["student", "professor"]:
            user = form.save()
            group = Group.objects.get(name=role)
            user.groups.add(group)
            
            login(request, user)
            return redirect('home')
    else:
        form = ExtendedSignupForm()
    return render(request, "register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect('login') 

def guest_login_view(request):
    user, created = User.objects.get_or_create(
        username='guest_visitor',
        defaults={
            'first_name': 'Guest',
            'last_name': 'User',
            'email': 'guest@example.com'
        }
    )
    
    guest_group, _ = Group.objects.get_or_create(name='guest')
    user.groups.add(guest_group)

    login(request, user)
    return redirect('home')