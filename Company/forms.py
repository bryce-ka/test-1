from django import forms
from .models import Job



class NewJobForm(forms.ModelForm):
    class Meta:
        model = Job
        # fields = ['title','job_type', 'company', 'location', 'department',  
        fields = ['role_sought', 'role_sought_other', 'company',  'location', 'location_other', 'funding_stage', 'funding_amount',
        'department', 'salary_range', 'title', 'job_type', 'remote', 'description', 'email', 'cloud', 'languages', 'property_type']
  
        
        help_texts = {
            'role_sought': "Select the category of the role youre recruiting for from the dropdown below.", 
            'role_sought_other': "If recruiting for another category, enter the category below.",
            'company': "Enter the name of the company you are recruiting for.",
            'location': "Choose from the following locations",
            'location_other': "If recruiting for another locaiton please enter the name of the location below.",
            'funding_stage' : "Please Select the stage of the funding secured for the company",
            'funding_amount': "Please Select the amount of the funding secured for the company",
            'department': "Please select the department for this role",
            
            'salary_range': "Please select a salary range for this role.",
            'title': "Enter the job title of the role you are recruiting for.",
            'job_type': "Is the role full or part time",
            'remote': "Is this a remote capable role?",
            'description': "Please enter a job description for the role. Text entered on seperate lines will be bulleted.",
            'email': 'If you want candidates to be able to email questions about the position, please provide an email address for candidates.',
           
            'cloud': "For Tech hires: Please select the cloud service used by this role", 
            'languages': "For Tech hires: Please select the prefered programing languague for this role", 
            
            'property_type': "For sales roles: Please Select the prefered property type for the position,", 
            
        }

class ViewJobForm_all(forms.ModelForm):
    class Meta:
        model = Job
        # fields = ['title','job_type', 'company', 'location', 'department',  
        fields = ['resume', 'job_type', 'remote', 'field_exp', 'proptech_exp', 'desired_salary']

        help_texts = {
            'resume' : "Upload your resume below", 
            'job_type': "Are you able to work full-tie or part-time?", 
            'remote': "Are you able to work remotely?",
            'field_exp': "How many years for experience do you have in the field", 
            'proptech_exp': "How many years of experience do you have in PropTech", 
            'desired_salary': "Enter your desired salary below", 
        }

class ViewJobForm_sales(forms.ModelForm):
    class Meta:
        model = Job 
        fields = ['resume','job_type', 'remote', 'field_exp', 'proptech_exp', 'desired_salary', 'property_type']

        help_texts = {
            'resume' : "Upload your resume below", 
            'job_type': "Are you able to work full-tie or part-time?", 
            'remote': "Are you able to work remotely?",
            'field_exp': "How many years for experience do you have in the field", 
            'proptech_exp': "How many years of experience do you have in PropTech", 
            'desired_salary': "Enter your desired salary below", 
            'property_type': "Select the property types you have experience with"
        }


class ViewJobForm_tech(forms.ModelForm):
    class Meta:
        model = Job
        # fields = ['title','job_type', 'company', 'location', 'department',  
        model = Job 
        fields = ['resume', 'job_type', 'remote','field_exp', 'proptech_exp', 'desired_salary', 'languages', 'cloud']

        help_texts = {
            'resume' : "Upload your resume below", 
            'job_type': "Are you able to work full-tie or part-time?", 
            'remote': "Are you able to work remotely?",
            'field_exp': "How many years for experience do you have in the field", 
            'proptech_exp': "How many years of experience do you have in PropTech", 
            'desired_salary': "Enter your desired salary below", 
            'languages': "Select the programming langugues you have experience with", 
            'cloud': "Select the cloud services you have experience with"
        }


class JobUpdateForm(forms.ModelForm):
    class Meta:
        model = Job
        # fields = ['title','job_type', 'company', 'location', 'department',  
        fields = ['role_sought', 'role_sought_other', 'company',  'location', 'location_other', 'funding_stage', 'funding_amount',
        'department', 'salary_range', 'title', 'job_type', 'remote', 'description', 'email', 'cloud', 'languages', 'property_type']
  
        
        help_texts = {
            'role_sought': "Select the category of the role youre recruiting for from the dropdown below.", 
            'role_sought_other': "If recruiting for another category, enter the category below.",
            'company': "Enter the name of the company you are recruiting for.",
            'location': "Choose from the following locations",
            'location_other': "If recruiting for another locaiton please enter the name of the location below.",
            'funding_stage' : "Please Select the stage of the funding secured for the company",
            'funding_amount': "Please Select the amount of the funding secured for the company",
            'department': "Please select the department for this role",
            
            'salary_range': "Please select a salary range for this role.",
            'title': "Enter the job title of the role you are recruiting for.",
            'job_type': "Is the role full or part time",
            'remote': "Is this a remote capable role?",
            'description': "Please enter a job description for the role. Text entered on seperate lines will be bulleted.",
            'email': 'If you want candidates to be able to email questions about the position, please provide an email address for candidates.',
           
            'cloud': "For Tech hires: Please select the cloud service used by this role", 
            'languages': "For Tech hires: Please select the prefered programing languague for this role", 
            
            'property_type': "For sales roles: Please Select the prefered property type for the position,", 
            
        }

    