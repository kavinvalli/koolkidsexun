from django.db import models
# Importing the default Django User Table 
from django.contrib.auth.models import User
#Imports for ckeditor
from ckeditor_uploader.fields import RichTextUploadingField
#Importing slugify for slugs
from django.utils.text import slugify
#Imports for taggit
from taggit.managers import TaggableManager

# class Job_functions(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField(null=True, blank=True)


class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Location(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

MALE=1
FEMALE=2
TRANSGENDER=3
PREFER_NOT_TO_SAY=4
gender_choices = (
    (MALE, "Male"),
    (FEMALE, "Female"),
    (TRANSGENDER, "Transgender"),
    (PREFER_NOT_TO_SAY, "Prefer Not To Say")
)

class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.IntegerField(choices=gender_choices)
    education = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name

FULL_TIME=1
PART_TIME=2
employment_type = (
    (FULL_TIME, 'Full Time'),
    (PART_TIME, 'Part Time')
)

GENERAL=1
LT_GENERAL=2
MAJOR=3
COLONEL=4
CADET=5
seniority_level = (
    (GENERAL, "General"),
    (LT_GENERAL, "Lt. General"),
    (MAJOR, "Major"),
    (COLONEL, "Colonel"),
    (CADET, "Cadet")
)

AVAILABLE=1
NOT_AVAILABLE=2
job_status = (
    (AVAILABLE, "Available"),
    (NOT_AVAILABLE, "Not Available")
)

class Jobs(models.Model):
    title = models.CharField(max_length=100)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    employment_type = models.IntegerField(choices=employment_type, default=1)
    seniority_level = models.IntegerField(choices=seniority_level, default=5)
    # job_functions = models.ManyToManyField(Job_functions, related_name='job_functions')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    applied_by = models.ManyToManyField(Applicant, related_name='applicants')
    description = RichTextUploadingField()
    taken_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.IntegerField(choices=job_status, default=1)
    slug = models.SlugField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            t_slug = slugify(self.title)
            startpoint = 1
            unique_slug = t_slug
            origin=1
            while Jobs.objects.filter(slug=unique_slug).exists():
                unique_slug = '{}-{}'.format(t_slug, origin)
                origin += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title