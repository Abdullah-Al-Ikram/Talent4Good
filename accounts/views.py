from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from accounts.forms import *
from projects.models import Project


# Create your views here.
@login_required
def index(request):
    projects = None
    if request.user.is_authenticated:
        projects = Project.objects.filter(organization_name=request.user)
    return render(request, 'index.html', {'projects': projects})

def login_user(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request=request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
    else:
        login_form = AuthenticationForm()
    return render(request, 'login.html', {'form': login_form})



def volunteer_register(request):
    if request.method == "POST":
        v_form = VolunteerForm(request.POST)
        if v_form.is_valid():
            user = v_form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('/')
    else:
        v_form = VolunteerForm()
    return render(request, 'volunteer-register.html', {'v_form': v_form})


def organization_register(request):
    if request.method == "POST":
        o_form = OrganizationForm(request.POST)
        if o_form.is_valid():
            user = o_form.save()
            login(request, user)
            messages.success(request, 'Account created successfully')
            return redirect('/')
    else:
        o_form = OrganizationForm()
    return render(request, 'organization-register.html', {'o_form': o_form})


@login_required
def profile(request):
    user = request.user
    profile = None
    if user.role == 'Volunteer':
        try:
            profile = user.volunteeruser
            if request.method == 'POST':
                volunteer_form = VolunteerProfileForm(request.POST, request.FILES, instance=profile)  # instance=profile, not user
                if volunteer_form.is_valid():
                    volunteer_form.save()
                    return redirect('profile')
            else:
                volunteer_form = VolunteerProfileForm(instance=profile)  # instance=profile
            return render(request, 'profile.html', {'profile': profile, 'volunteer_form': volunteer_form})
        except VolunteerUser.DoesNotExist:
            profile = None
    elif user.role == 'Organization':
        try:
            profile = user.organizationuser
            if request.method == 'POST':
                organization_form = OrganizationProfileForm(request.POST, request.FILES, instance=profile)  # instance=profile, not user.organizationuser
                if organization_form.is_valid():
                    organization_form.save()
                    return redirect('profile')
            else:
                organization_form = OrganizationProfileForm(instance=profile)
            return render(request, 'profile.html', {'profile': profile, 'organization_form': organization_form})
        except OrganizationUser.DoesNotExist:
            profile = None
    if profile is None:
        return render(request, 'profile.html', {'error': 'Profile not found or incomplete.'})

    return render(request, 'profile.html', {'profile': profile})


def logout_user(request):
    logout(request)
    messages.success(request, 'Logout successful')
    return redirect('/')