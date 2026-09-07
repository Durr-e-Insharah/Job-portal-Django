from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Job, Application
from .forms import JobForm


class JobListView(ListView):
    model = Job
    template_name = 'job_list.html'
    context_object_name = 'all_jobs'


class JobDetailView(DetailView):
    model = Job
    template_name = 'job_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['already_applied'] = Application.objects.filter(
                job=self.object, applicant=self.request.user
            ).exists()
        return context


class JobCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Job
    form_class = JobForm
    template_name = 'job_form.html'
    success_url = reverse_lazy('job_list')

    def test_func(self):
        return self.request.user.role == 'employer'

    def form_valid(self, form):
        form.instance.posted_by = self.request.user
        return super().form_valid(form)


class JobUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Job
    form_class = JobForm
    template_name = 'job_form.html'
    success_url = reverse_lazy('job_list')

    def test_func(self):
        return self.get_object().posted_by == self.request.user


class JobDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Job
    template_name = 'job_confirm_delete.html'
    success_url = reverse_lazy('job_list')

    def test_func(self):
        return self.get_object().posted_by == self.request.user


class MyJobsListView(LoginRequiredMixin, ListView):
    model = Job
    template_name = 'my_jobs.html'
    context_object_name = 'my_jobs'

    def get_queryset(self):
        return Job.objects.filter(posted_by=self.request.user)


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk)
    Application.objects.get_or_create(job=job, applicant=request.user)
    return redirect('job_detail', pk=pk)


class MyApplicationsListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'my_applications.html'
    context_object_name = 'my_applications'

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)