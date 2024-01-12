from django.contrib import admin
from .models import ChildProfile, HealthProfessionalProfile,ParentProfile
# Register your models here.
admin.site.register(HealthProfessionalProfile)
admin.site.register(ParentProfile)
admin.site.register(ChildProfile)