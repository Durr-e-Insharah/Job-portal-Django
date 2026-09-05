# Register your models here.
from django.contrib import admin
from .models import Job, Application

class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'location', 'salary', 'posted_by', 'created_at']
    list_filter = ['company', 'location']
    search_fields = ['title', 'company']

class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['job', 'applicant', 'applied_at']

admin.site.register(Job, JobAdmin)
admin.site.register(Application, ApplicationAdmin)