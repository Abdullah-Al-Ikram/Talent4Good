from django.contrib.auth.forms import UserCreationForm
from .models import *
from django import forms

class VolunteerForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'Volunteer'
        if commit:
            user.save()
            VolunteerUser.objects.create(user=user)
        return user

class OrganizationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'Organization'
        if commit:
            user.save()
            OrganizationUser.objects.create(user=user)
        return user


class VolunteerProfileForm(forms.ModelForm):
    class Meta:
        model = VolunteerUser
        fields = ['name', 'skills', 'portfolio_link', 'experience', 'image', 'available']

class OrganizationProfileForm(forms.ModelForm):
    class Meta:
        model = OrganizationUser
        fields = ['organization_name', 'description', 'website', 'image']