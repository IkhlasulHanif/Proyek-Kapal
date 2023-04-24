from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Ship, Block

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            role = form.cleaned_data.get('role')
            user = form.save(commit=False)
            user.role = role
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    return render(request, 'login.html')

@login_required
def home(request):
    if request.user.role == 'inspector':
        return render(request, 'inspector/role_home.html')
    elif request.user.role == 'repairmen':
        return render(request, 'repairmen/role_home.html')
    elif request.user.role == 'admin':
        return render(request, 'admin/role_home.html')
    else:
        # If user's role is not recognized, return a default home page
        return render(request, 'home.html')

@login_required
def add_ship(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            messages.error(request, 'Please enter a name')
            return redirect('add_ship')
        else:
            ship = Ship.objects.create(name=name)
            messages.success(request, f'{name} added successfully')
            return redirect('ship_detail', pk=ship.pk)
    else:
        return render(request, 'admin/add_ship.html')