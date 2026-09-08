from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Job, Application
from .forms import JobForm, ApplicationForm


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

    if Application.objects.filter(job=job, applicant=request.user).exists():
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            return redirect('job_detail', pk=pk)
    else:
        form = ApplicationForm()

    return render(request, 'apply_job.html', {'form': form, 'job': job})


class MyApplicationsListView(LoginRequiredMixin, ListView):
    model = Application
    template_name = 'my_applications.html'
    context_object_name = 'my_applications'

    def get_queryset(self):
        return Application.objects.filter(applicant=self.request.user)


class JobApplicantsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Application
    template_name = 'job_applicants.html'
    context_object_name = 'applicants'

    def test_func(self):
        self.job = get_object_or_404(Job, pk=self.kwargs['pk'])
        return self.job.posted_by == self.request.user

    def get_queryset(self):
        return Application.objects.filter(job=self.job)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['job'] = self.job
        return context