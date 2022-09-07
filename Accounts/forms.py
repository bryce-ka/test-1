from django import forms 
from localflavor.us.us_states import STATE_CHOICES
from Accounts.models import CustomUser as User
from django import forms
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm as BaseAuthenticationForm
from django.contrib.auth.forms import PasswordResetForm as BasePasswordResetForm
from django.contrib.auth.forms import SetPasswordForm as BaseSetPasswordForm
from django.contrib.auth.forms import UsernameField
from django.contrib.auth import password_validation
from django.utils.translation import gettext, gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from Accounts.admin import UserCeationForm, UserChangeForm
from django.contrib.auth.hashers import make_password



class CandidateFormNew(UserCeationForm):
    
    class Meta:
        model = User
        fields = ("user_name", "first_name", "last_name", "email", "country", "location", "location_other", "resume", "tech_lang", 
        "tech_cloud", "property_type", "role_sought", "desired_salary_range", "remote_capable",  "desired_time", 'field_experience', 'proptech_experience', "is_candidate", )
        widgets = {'is_candidate': forms.HiddenInput()}
        
    def save(self):
        data = self.cleaned_data
        this_user = User(user_name = data['user_name'], first_name=data['first_name'], last_name=data['last_name'], email = data['email'], country = data['country'], 
        location= data['location'], location_other= data['location_other'], resume = data['resume'], tech_lang= data['tech_lang'], tech_cloud= data['tech_cloud'],
        property_type = data['property_type'], role_sought = data['role_sought'], desired_salary_range= data['desired_salary_range'], remote_capable= data['remote_capable'],
        desired_time = data['desired_time'], field_experience = data['field_experience'], proptech_experience = data['proptech_experience'], is_candidate= True, 
        password = make_password(data['password1']))
        this_user.save()



class RecruiterFormNew(UserCeationForm):
    class Meta:
        model = User
        fields = ( "email", "user_name", "first_name", "last_name", "company", "location", "location_other", "country", "funding_stage", "funding_amount", "is_recruiter")
        widgets = {'is_recruiter': forms.HiddenInput()}
    def save(self):
        data = self.cleaned_data
        this_user = User(email=data['email'], user_name = data['user_name'], first_name=data['first_name'], last_name=data['last_name'], company= data['company'], 
        location= data['location'], location_other= data['location_other'], country = data['country'], funding_stage = data['funding_stage'], 
        funding_amount = data['funding_amount'], is_recruiter = True, password=make_password(data['password1']),)
        this_user.save()

# class ProfileUpdateForm(UserChangeForm):
#     class Meta:
#         model = User
#         fields = [ "email", 'company', "first_name", "last_name", 'password', "location", "location_other", "country","resume", "tech_lang", 
#         "tech_cloud", "property_type", "role_sought", "desired_salary_range", "remote_capable",  "desired_time", 'field_experience', 'proptech_experience']

   
#         help_texts = {
#             'field_exp': "How many years of experience do you have the field.", 
#             'proptech_exp':"How many years of experience do you have in PropTech.", 
#             'tech_lang': "For Tech hires: Please select the programming languagues you are experienced with.", 
#             'tech_cloud': "For Tech hires: Please select the cloud service used by this role.", 
#             'property_type': "For sales roles: Please Select the prefered property type for the position.", 
#             'desired_time': "are you looking for a full or part time the role full or part time",
#         }

class AuthenticationForm(BaseAuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={
        'autofocus': True,
        'class': 'form-control',
        'placeholder': _('Enter username')
    }))
    password = forms.CharField(label=_("Password"), strip=False,
                               widget=forms.PasswordInput(attrs={
                                   'autocomplete': 'current-password',
                                   'class': 'form-control'
                               }))


class PasswordResetForm(BasePasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'autofocus': True})
    )


class SetPasswordForm(BaseSetPasswordForm):
    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control', 'autofocus': True}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'off', 'class': 'form-control'}),
    )


class PasswordChangeForm(SetPasswordForm):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control'}),
    )

