from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.views.generic.base import TemplateView
from django.views.generic import ListView
from .models import Jobs, Applicant
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User

class LandingPageView(TemplateView):
    template_name = 'jobs/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["home"]="active"
        return context

class AboutPageView(TemplateView):
    template_name = 'jobs/about.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["about"]="active"
        return context

class PerksPageView(TemplateView):
    template_name = 'jobs/perks.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["perks"]="active"
        return context

class JobPageView( LoginRequiredMixin, ListView):
    # model=Jobs
    login_url='/login/'
    redirect_field_name='redirect_to'
    queryset = Jobs.objects.filter(status=1)
    context_object_name = 'jobs'
    template_name='jobs/jobs.html'
    paginate_by=10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user=self.request.user
        applicant=Applicant.objects.get(user=user)
        applied_jobs = Jobs.objects.filter(applied_by__in=[applicant])
        context["applied_jobs"]=applied_jobs
        context["userjob"]="active"
        return context
# def index(request, user_id):
#     user = User.objects.get(id=user_id)
#     response = 'Hello '+user.username
#     return HttpResponse(response)

def specific_job(request, user_id, job_id):
    if request.method=="GET":
        jobs = Jobs.objects.filter(status=1).exclude(id=job_id).order_by('?')[:10]
        job = Jobs.objects.get(pk=job_id)
        user = User.objects.get(pk=user_id)
        applicant = Applicant.objects.get(user=user)
        applied_jobs = Jobs.objects.filter(applied_by__in=[applicant])
        context = {
            'job':job,
            'jobs':jobs,
            'applied_jobs':applied_jobs,
            'userjob':'active',
        }
        return render(request, 'jobs/job.html', context)
    elif request.method == 'POST':
        userid = request.POST.get('userid')
        jobid = request.POST.get('jobid')
        job = Jobs.objects.get(id=jobid)
        user = User.objects.get(pk=userid)
        applicant = Applicant.objects.get(user=user)
        job.applied_by.add(applicant)
        job.save()
        url = '/jobs/'+userid+'/jobs/'
        return redirect(url)

def jobstatus(request, user_id):
    user = User.objects.get(pk=user_id)
    applicant = Applicant.objects.get(user=user)
    applied_open_jobs = Jobs.objects.filter(applied_by__in=[applicant], status=1)
    applied_closed_jobs = Jobs.objects.filter(applied_by__in=[applicant], status=2).exclude(taken_by=user)
    recruited_jobs = Jobs.objects.filter(taken_by=user)
    context = {
        'userjob':'active',
        'applied_open_jobs':applied_open_jobs,
        'applied_closed_jobs':applied_closed_jobs,
        'recruited_jobs':recruited_jobs,
    }
    return render(request, 'jobs/jobstatus.html',context)

def profile(request, user_id):
    if request.method=="GET":
        user = User.objects.get(pk=user_id)
        applicant = Applicant.objects.get(user=user)
        context = {
            # 'userjob':'active',
            'applicant':applicant,
            'user':user,
        }
        return render(request, 'jobs/profile.html',context)
    elif request.method=="POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        education = request.POST.get('education')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        user = User.objects.get(pk=user_id)
        applicant = Applicant.objects.get(user=user)
        user.first_name = first_name
        user.last_name = last_name
        applicant.age = age
        applicant.gender = gender
        applicant.education = education
        user.email = email
        applicant.mobile = mobile
        user.save()
        applicant.save()
        url="/jobs/"+str(user_id)+"/profile/"
        return redirect(url)