from django.contrib import admin
from .models import Skills, AppliedJobs, SavedJobs

# Register your models here.

admin.site.register(Skills)
admin.site.register(AppliedJobs)
admin.site.register(SavedJobs)