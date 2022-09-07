from django.db import models
from Accounts.models import CustomUser as User
from django.utils import timezone
from autoslug import AutoSlugField
from django.utils import timezone
from multiselectfield import MultiSelectField

CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
)
DEPARTMENT = (
    ('Engineering', 'Engineering'),
    ('Product', 'Product'),
    ('Marketing','Marketing'),
    ('Sales', 'Sales'),
    ('Operations', 'Operations'),
    ('Other', 'Other'),
)
TECH_LANGUAGES = (
    ('Java', 'Java'),
    ('C++', 'C++'),
    ('Python','Python'),
)
LOCATION = (
    ('New York', 'New York'),
    ('London', 'London'),
    ('Los Angeles','Los Angeles'),
    ('San Francisco', 'San Francisco'),
    ('Seattle', 'Seattle'),
    ('Chicago', 'Chicago'),
    ('Remote', 'Remote'),
    ('Other', 'Other')
)
CLOUD = (
    ('AWS', 'AWS'),
    ('GCP', 'GCP'),
    ('Azure','Azure'),
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
    ('Data Engineering', 'Data Engineering'),
    ('Data Science', 'Data Science'),
    ('Engineering', 'Engineering'),
    ('Front End Engineer', 'Front End Engineer'),
    ('Product Management','Product Management'),
    ('Sales Entry','Sales Entry'),
    ('Sales Exec', 'Sales Exec'),
    ('Sales Mid-level', 'Sales Mid-level'),
    ('UX Designer', 'UX Designer'),
    ('Other', 'Other'),
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
    ('Yes', True), 
    ('No', False),
)
FUNDING_STAGE =(
    ('Seed Round', 'Seed Round'),
    ('Post Seed', 'Post Seed'),
    ('A Round','A Round'),
    ('B Round', 'B Round'),
    ('C Round ', 'C Round '),
    ('Late Stage (post C)', 'Late Stage (post C)'),
    ('Public', 'Public'),
)
FUNDING_AMOUNT =(
    ('<$1M', '<$1M'),
    ('$1m - $2m','$1m - $2m'),
    ('$2m - $5m', '$2m - $5m'),
    ('$5m - $10m', '$5m - $10m'),
    ('$10m - $20m', '$10m - $20m'),
    ('$20m - $50m', '$20m - $50m'),
    ('$50m+', '$50m+'),
)

class Job(models.Model):
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, null=True)
    recruiter = models.ForeignKey(User, related_name='jobs', on_delete=models.CASCADE)
    role_sought = models.CharField(max_length = 80,choices=ROLE_SOUGHT, null=False)
    role_sought_other = models.CharField(max_length=100, null=True, blank = True)
    company = models.CharField(max_length=200, null = False)
    location = models.CharField(max_length = 50, choices=LOCATION, null=False)
    location_other = models.CharField(max_length = 100, null=True,  blank=True)
    funding_stage = models.CharField(max_length = 50, choices=FUNDING_STAGE, null=False)
    funding_amount = models.CharField(max_length = 12, choices=FUNDING_AMOUNT, null=False)
    department = models.CharField(max_length = 50, choices=DEPARTMENT, null=False)
    
    salary_range = models.CharField(max_length = 50, choices=SALARY_RANGE, null=True)
    
    job_type= models.CharField(choices=CHOICES, default='Full Time', max_length=30, null=True)
    remote = models.CharField(max_length = 20, choices=REMOTE_CAPABLE, null=False)
    description = models.TextField()
    email = models.EmailField(null=True, blank =True)
    date_posted = models.DateTimeField(default=timezone.now)
    last_edit = models.DateTimeField(default=timezone.now)

    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    field_exp = models.IntegerField(null = False, default = 0)
    proptech_exp = models.IntegerField(null = False, default = 0)
    desired_salary = models.IntegerField(null=True, blank=True)
    

    cloud = MultiSelectField(choices=CLOUD, null=True, blank=True)
    languages = MultiSelectField(choices=TECH_LANGUAGES, null=True, blank =True)
    
    property_type = MultiSelectField(choices=PROPERTY_TYPE, null=True, blank = True)
    
    
    skills_req = models.CharField(max_length=200)

    
    def __str__(self):
        return self.title


class Applicants(models.Model):
    job = models.ForeignKey(
        Job, related_name='applicants', on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name='applied', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.applicant


class Selected(models.Model):
    job = models.ForeignKey(
        Job, related_name='select_job', on_delete=models.CASCADE)
    applicant = models.ForeignKey(
        User, related_name='select_applicant', on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.applicant


