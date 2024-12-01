from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
# Create your views here.
def home(request):
    projects = Project.objects.all()[:3]
    return render(request, 'home.html', {'projects': projects})

@login_required
def view_projects(request):
    projects = Project.objects.all()
    return render(request, 'projects/view_projects.html', {'projects': projects})

@login_required
def user_applied_projects(request):
    # Get all applications made by the current user
    applications = ProjectApplication.objects.filter(user=request.user)

    return render(request, 'projects/user_applied_projects.html', {'applications': applications})


@login_required
def apply_for_project(request, project_id):
    project = Project.objects.get(id=project_id)
    projects = Project.objects.all()
    if request.method == 'POST':
        form = ProjectApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.project = project
            application.user = request.user
            application.status = 'Pending'
            application.save()
            return redirect('projects:user_applied_projects')
        else:
            return render(request, 'projects/apply_for_project.html', {'form': form, 'project': project, 'projects': projects})
    else:
        form = ProjectApplicationForm()
    return render(request, 'projects/apply_for_project.html', {'form': form, 'project': project, 'projects': projects})

@login_required
def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            # Create a project instance from the form data
            project = form.save(commit=False)  # Don't save yet, we need to set the organization_name
            project.organization_name = request.user  # Assign the logged-in user as the organization
            project.save()  # Now save the project
            return redirect('index')  # Redirect to the view projects page
        else:
            print("Form is invalid:", form.errors)  # Debugging line to print errors
            return render(request, 'projects/add_project.html', {'form': form})
    else:
        # Initialize the form with the logged-in user as the organization_name field
        form = ProjectForm(initial={'organization_name': request.user})
    return render(request, 'projects/add_project.html', {'form': form})

@login_required
def view_applications(request, project_id):
    project = Project.objects.get(id=project_id)
    if project.organization_name != request.user:
        return redirect('projects:view_projects')
    applications = ProjectApplication.objects.filter(project=project)
    return render(request, 'projects/view_applications.html', {'project': project, 'applications': applications})



@login_required
def change_application_status(request, application_id, action):
    application = ProjectApplication.objects.get(id=application_id)
    if application.project.organization_name != request.user:
        return redirect('projects:view_projects')

    if action == 'accept':
        application.status = 'Accepted'
    elif action == 'reject':
        application.status = 'Rejected'
    application.save()
    return redirect('projects:view_applications', project_id=application.project.id)


@login_required
def view_applications(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if project.organization_name != request.user:
        return redirect('error_page')
    applications = ProjectApplication.objects.filter(project=project)
    return render(request, 'projects/view_applications.html', {'project': project, 'applications': applications})