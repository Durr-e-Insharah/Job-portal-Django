from django.urls import path
from . import views

urlpatterns = [
    path('', views.JobListView.as_view(), name='job_list'),
    path('job/<int:pk>/', views.JobDetailView.as_view(), name='job_detail'),
    path('job/new/', views.JobCreateView.as_view(), name='job_create'),
    path('job/<int:pk>/edit/', views.JobUpdateView.as_view(), name='job_update'),
    path('job/<int:pk>/delete/', views.JobDeleteView.as_view(), name='job_delete'),
    path('my-jobs/', views.MyJobsListView.as_view(), name='my_jobs'),
    path('job/<int:pk>/apply/', views.apply_job, name='apply_job'),
    path('my-applications/', views.MyApplicationsListView.as_view(), name='my_applications'),
]