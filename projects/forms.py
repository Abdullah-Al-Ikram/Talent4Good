from django import forms
from .models import *


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['organization_name', 'title', 'description', 'skills', 'duration', 'image', 'status']

    # Optional: Add a custom save method to handle logic for the ForeignKey field
    def save(self, commit=True):
        # Ensure that the organization_name is set to the logged-in user when saving
        instance = super().save(commit=False)
        if not instance.organization_name:
            instance.organization_name = self.initial.get('organization_name',
                                                          None)  # Ensure it's set from the initial data
        if commit:
            instance.save()
        return instance

class ProjectApplicationForm(forms.ModelForm):
    class Meta:
        model = ProjectApplication
        fields = ['project', 'fullname', 'description', 'cover_letter', 'image']