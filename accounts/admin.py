from django.contrib import admin
from .models import *
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.role == 'volunteer':
            VolunteerUser.objects.get_or_create(user=obj)
        elif obj.role == 'organization':
            OrganizationUser.objects.get_or_create(user=obj)

admin.site.register(User)
admin.site.register(VolunteerUser)
admin.site.register(OrganizationUser)