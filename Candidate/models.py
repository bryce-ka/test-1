from django.db import models
from Accounts.models import CustomUser as User
from django.utils import timezone
from autoslug import AutoSlugField
from Company.models import Job
from django.utils import timezone
from multiselectfield import MultiSelectField

# Create your models here.

CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Internship', 'Internship'),
    ('Temporary','Temporary'),
    ('Remote', 'Remote'),
)

LOCATION = (
    ('New York', 'New York'),
    ('London', 'London'),
    ('Los Angeles','Los Angeles'),
    ('San Francisco', 'San Francisco'),
    ('Operations', 'Operations'),
    ('Seattle', 'Seattle'),
    ('Chicago', 'Chicago'),
    ('Remote', 'Remote'),
)

TECH_LANGUAGES = (
    ('Java', 'Java'),
    ('C++', 'C++'),
    ('Python','Python'),
)

CLOUD = (
    ('AWS', 'AWS'),
    ('GCP', 'GCP'),
    ('Azure','Azure'),
    ('n/a', 'n/a'),
)
PROPERTY_TYPE = (
    ('Multifamily', 'Multifamily'),
    ('Retail', 'Retail'),
    ('Office','Office'),
    ('Industrial', 'Industrial'),
    ('Hotel', 'Hotel'),
    ('Other', 'Other'),
)
ROLE_SOUGHT = (
    ('C Suite', 'C Suite'),
    ('Sales Exec', 'Sales Exec'),
    ('Sales Entry','Sales Entry'),
    ('Sales Mid-level', 'Sales Mid-level'),
    ('Front End Engineer', 'Front End Engineer'),
    ('UX Designer', 'UX Designer'),
    ('Data Engineerg', 'Data Engineerg'),
    ('Data Science', 'Data Science'),
    ('Product Management','Product Management'),
    ('Engineering', 'Engineering'),
)
SALARY_RANGE = (
    ('$50k - $75k', '$50k - $75k'),
    ('$75k - $100k', '$75k - $100k'),
    ('$100k - $125k','$100k - $125k'),
    ('$125k - $175k', '$125k - $175k'),
    ('$175k - $200k', '$175k - $200k'),
    ('$200k+', '$200k+'),
    ('Commision-based', 'Commision-based'),
)
REMOTE_CAPABLE = (
    ('Yes', 'Yes'), 
    ('No', 'No'),
)


class Skills(models.Model):
    skill = models.CharField(max_length=200)
    
    user = models.ForeignKey(
        User, related_name='skills', on_delete=models.CASCADE)
    

class SavedJobs(models.Model):
    job = models.ForeignKey(
        Job, related_name='saved_job', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='saved', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.job.title

class AppliedJobs(models.Model):
    job = models.ForeignKey(
        Job, related_name='applied_job', on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name='applied_user', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.job.title 