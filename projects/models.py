from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
# Create your models here.

class Project(models.Model):
    organization_name = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects"
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    skills = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    image = models.ImageField(upload_to="projects/images/", null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.title

class ProjectApplication(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    fullname = models.CharField(max_length=255)
    description = models.TextField()
    cover_letter = models.FileField(upload_to="applications/cover_letters/")
    image = models.ImageField(upload_to="applications/images/", null=True, blank=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Application by {self.fullname} for {self.project.title}"
