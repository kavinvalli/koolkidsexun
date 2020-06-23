from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.http import HttpResponse
from jobs.models import *
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from django.shortcuts import reverse
from django.shortcuts import redirect, get_object_or_404

def superuser(user):
    return user.is_superuser == True

def master(request):
    if request.method=="POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser == True:
            login(request, user)
            url = "/master/loggedin"
            return redirect(url)
            # return HttpResponse("Hello ADMIN")
        elif user is None:
            return render(request, "login/login.html", {"message": "Invalid credentials."})
        elif user.is_superuser == False:
            return render(request, "login/login.html", {"message": "You're not the Admin"}) 
        else:
            return render(request, "login/login.html", {"message": "Invalid credentials."})
    else:
        return render(request, "login/login.html", {"message": None, 'action_url':'/master/'})

@user_passes_test(superuser, login_url='/master/')
def loggedin(request):
    total_jobs = Jobs.objects.all()
    taken_jobs = Jobs.objects.filter(status=2)
    open_jobs = Jobs.objects.filter(status=1)
    users = User.objects.all()
    jobs_applied = Jobs.objects.filter(status=1).exclude(applied_by=None).order_by('-id')[:5]
    context = {
        'total_jobs': total_jobs,
        'taken_jobs': taken_jobs,
        'open_jobs': open_jobs,
        'users': users,
        'jobs_applied':jobs_applied,
    }
    return render(request, "master/landing.html", context)

@user_passes_test(superuser, login_url='/master/')
def jobs(request):
    if request.method == "GET":
        jobs = Jobs.objects.all()
        context = {
            'jobs':jobs,
        }
        return render(request, 'master/jobs.html', context)

@user_passes_test(superuser, login_url='/master/')
def add_job(request):
    if request.method == "GET":
        locations = Location.objects.all()
        departments = Department.objects.all()
        context = {
            'locations': locations,
            'departments': departments,
        }
        return render(request, 'master/add-job.html', context)
    if request.method=="POST":
        title = request.POST.get("title")
        location_id = request.POST.get("location")
        location = Location.objects.get(pk=location_id)
        employment_type = request.POST.get("employment_type")
        seniority_level = request.POST.get("seniority_level")
        department_id = request.POST.get("department")
        department = Department.objects.get(pk=department_id)
        description = request.POST.get("description")
        Jobs.objects.create(
            title=title,
            location=location,
            employment_type=employment_type,
            seniority_level=seniority_level,
            department=department,
            description=description,
            status=1,
        )
        url = "/master/loggedin/jobs"
        return redirect(url)

@user_passes_test(superuser, login_url='/master/')
def edit_job(request, job_id):
    if request.method == 'GET':
        job = Jobs.objects.get(pk=job_id)
        locations = Location.objects.all()
        departments = Department.objects.all()
        context = {
            'job':job,
            'locations': locations,
            'departments': departments,
        }
        return render(request, 'master/edit-job.html', context)
    else:
        job = Jobs.objects.get(pk=job_id)
        title = request.POST.get("title")
        location_id = request.POST.get("location")
        location = Location.objects.get(pk=location_id)
        employment_type = request.POST.get("employment_type")
        seniority_level = request.POST.get("seniority_level")
        department_id = request.POST.get("department")
        department = Department.objects.get(pk=department_id)
        description = request.POST.get("description")
        job.title=title
        job.location=location
        job.employment_type=employment_type
        job.seniority_level=seniority_level
        job.department=department
        job.description=description
        job.save()
        url="/master/loggedin/jobs"
        return redirect(url)

@user_passes_test(superuser, login_url='/master/')
def applied(request):
    if request.method=="GET":
        jobs_applied = Jobs.objects.filter(status=1).exclude(applied_by=None)
        context = {
            'jobs_applied': jobs_applied,
        }
        return render(request, 'master/applied.html', context)

@user_passes_test(superuser, login_url='/master/')
def specific_applied(request, job_id):
    if request.method=="GET":
        job = Jobs.objects.get(pk=job_id, status=1)
        context = {
            'job_applied': job,
        }
        return render(request, 'master/specific_applied.html', context)

@user_passes_test(superuser, login_url='/master/')
def applicant(request, applicant_id):
    if request.method=="GET":
        applicant = Applicant.objects.get(pk=applicant_id)
        jobs = Jobs.objects.filter(applied_by__in=[applicant], status=1)
        context = {
            'applicant': applicant,
            'jobs':jobs
        }
        return render(request, 'master/applicant.html', context)

@user_passes_test(superuser, login_url='/master/')
def recruit(request):
    if request.method=="POST":
        jobid = request.POST.get('job')
        applicantid = request.POST.get('applicant')
        job = Jobs.objects.get(pk=jobid)
        applicant = Applicant.objects.get(pk=applicantid)
        user=applicant.user
        job.status=2
        job.taken_by = user
        job.save()

        to_email = user.email
        email_subject = "You've been recruited!!!"
        message = render_to_string('master/recruited.html', {
            'user': user,
        })
        email = EmailMessage(email_subject, message, "Kool Kids Klub Resistance Fighting Force <info@foop.com>", to=[to_email])
        email.send()

        url = "/master/loggedin/applicant/"+applicantid
        return redirect(url)

@user_passes_test(superuser, login_url='/master/')
def add_location(request):
    if request.method=="GET":
        return render(request, 'master/add-location.html')
    elif request.method=="POST":
        name=request.POST.get("name")
        Location.objects.create(
            name=name
        )
        url="/master/loggedin/add-location/"
        return redirect(url)

@user_passes_test(superuser, login_url='/master/')
def add_department(request):
    if request.method=="GET":
        return render(request, 'master/add-department.html')
    elif request.method=="POST":
        name=request.POST.get("name")
        Department.objects.create(
            name=name
        )
        url="/master/loggedin/add-department/"
        return redirect(url)

@user_passes_test(superuser, login_url='/master/')
def recruited_jobs(request):
    recruited_jobs = Jobs.objects.filter(status=2)
    context = {
        'recruited_jobs':recruited_jobs,
    }
    return render(request, 'master/recruited-jobs.html', context)