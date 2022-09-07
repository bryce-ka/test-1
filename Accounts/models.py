#for custom user
from multiprocessing.sharedctypes import Value
from random import choices
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.forms import CharField, ValidationError
from django.utils import timezone
from autoslug import AutoSlugField
from django.utils import timezone
from multiselectfield import MultiSelectField
from django.utils.translation import gettext_lazy as lazy
from django_countries.fields import CountryField
from django.utils.text import slugify

# Create your models here.

CHOICES = (
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Temporary','Temporary'),
    ('Remote', 'Remote'),
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

TECH_LANGUAGES = (
    ('Java', 'Java'),
    ('C++', 'C++'),
    ('Python','Python'),
    ('Other', 'Other')
)

CLOUD = (
    ('AWS', 'AWS'),
    ('GCP', 'GCP'),
    ('Azure','Azure'),
    ('Other', 'Other')
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
    ('Other', 'Other')
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

class CustomAccountManager(BaseUserManager):
    
    def create_superuser(self, email, user_name, first_name, password, **other_fields):
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError('Super user must be assigned to is_staff = True.')
        if other_fields.get("is_superuser") is not True:
            raise ValueError('Super user must be assigned to  = True.')

        return self.create_user( email, user_name, first_name, password, **other_fields)
    
    def create_user(self, email, user_name, first_name, password, **other_fields):
        if not email:
            raise ValueError(lazy("You must provide a valid email address"))
        email = self.normalize_email(email)
        if not first_name:
            raise ValueError(lazy("You must provide a valid first name"))
        if not password or len(password) <7:
            raise ValueError(lazy("You must provide a valid password withat least 8 characters"))

        user = self.model( email=email, user_name= user_name, first_name=first_name, **other_fields )
        user.set_password(password)
        user.save()
        return user

    
        

class CustomUser(AbstractBaseUser, PermissionsMixin, models.Model):
    email = models.EmailField(lazy("email address"),unique=True)
    user_name = models.CharField( max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank = True)
    last_name = models.CharField(max_length=150, blank = True)
    is_recruiter = models.BooleanField(default = False)
    is_candidate = models.BooleanField(default = False)
    country = CountryField(null=True, blank=True)
    location =  models.CharField(max_length = 50, choices = LOCATION, null= False, blank=False)
    location_other = models.CharField(max_length = 50, null= True, blank=True)
    company = models.CharField(max_length=100, null=True, blank = True)
    resume = models.FileField(upload_to='resumes', null=True, blank=True)
    tech_lang = MultiSelectField(choices = TECH_LANGUAGES,  null=True, blank=True)
    tech_cloud = MultiSelectField(choices=CLOUD, null=True, blank=True)
    property_type = MultiSelectField(choices=PROPERTY_TYPE, null=True, blank = True)
    role_sought =  MultiSelectField(choices=ROLE_SOUGHT, null=True, blank = True)
    desired_salary_range = models.CharField(max_length = 100, choices=SALARY_RANGE, null= True, blank = True)
    remote_capable = models.CharField(max_length = 100,choices=REMOTE_CAPABLE, null= True, blank = True)
    desired_time = models.CharField(max_length = 100,choices=CHOICES, null= True, blank = True)
    funding_stage = models.CharField(max_length = 100,choices=FUNDING_STAGE, null= True, blank = True)
    funding_amount = models.CharField(max_length = 100,choices= FUNDING_AMOUNT, null= True, blank = True)
    proptech_experience = models.IntegerField(null= True, blank = True, default = 0)
    field_experience= models.IntegerField(null= True, blank = True, default = 0)
    slug = AutoSlugField(populate_from='email', unique=True)
    is_staff = models.BooleanField(default = False)
    is_active = models.BooleanField(default = True) ## change for email validation sending a link 
    objects = CustomAccountManager()

    class Meta:
        verbose_name = lazy('user')
        verbose_name_plural = lazy('users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["user_name", "first_name"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    
    def get_absolute_url(self):
        return "/profile/{}".format(self.slug)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return str(self.email)
    

# class Company(models.Model):
#     name = models.CharField(max_length=100)
#     recruiter1 = models.ForeignKey(CustomUser, null=True, blank =True)
#     recruiter2 = models.ForeignKey(CustomUser, null=True, blank =True)
#     recruiter3 = models.ForeignKey(CustomUser, null=True, blank =True)
#     def __str__(self):
#         return self.name



