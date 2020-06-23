from django.urls import path
from . import views

urlpatterns = [
    path('', views.master, name='master'),
    path('loggedin/', views.loggedin, name='loggedin'),
    path('loggedin/jobs', views.jobs, name='jobs'),
    path('loggedin/add-job', views.add_job, name='add-job'),
    path('loggedin/edit-job/<int:job_id>', views.edit_job, name='edit-job'),
    path('loggedin/applied-jobs', views.applied, name='applied'),
    path('loggedin/applied-jobs/<int:job_id>', views.specific_applied, name='specific-applied'),
    path('loggedin/applicant/<int:applicant_id>', views.applicant, name='applicant'),
    path('loggedin/recruit/', views.recruit, name='recruit'),
    path('loggedin/recruited-jobs/', views.recruited_jobs, name='recruited-jobs'),
    path('loggedin/add-location/', views.add_location, name='add-location'),
    path('loggedin/add-department/', views.add_department, name='add-department'),
]