from django.urls import path
from . import views
from django.views.generic.base import RedirectView

urlpatterns = [
    path('<int:user_id>/', RedirectView.as_view(url='jobs/', permanent=False)),
    path('<int:user_id>/jobs/', views.JobPageView.as_view(), name='user_all_jobs'),
    path('<int:user_id>/jobs/<int:job_id>', views.specific_job, name='user_specific_job_details'),
    path('<int:user_id>/job-status/', views.jobstatus, name='jobstatus'),
    path('<int:user_id>/profile/', views.profile, name='profile'),
]