from django import forms 
from django.contrib import admin
from django.contrib.auth.models import Group
from Accounts.models import CustomUser
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

class UserCeationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = ("user_name", "email", "first_name", "last_name", 'password1', 'password2', "location", "location_other", "country", )

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password("password1")
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ("user_name", "email", 'company', "first_name", "last_name", 'password', "location", "location_other", "country","resume", "tech_lang", 
        "tech_cloud", "property_type", "role_sought", "desired_salary_range", "remote_capable",  "desired_time", 'field_experience', 'proptech_experience')

class UserAdminConfig(BaseUserAdmin):
    search_fields = ('email', 'first_name', 'company',)
    ordering=('email',)
    list_display= ('email', 'is_recruiter', 'company', 'is_active',)
    fieldsets = (
        ('Registration Info', {'fields': ( "user_name", "email", "first_name", "last_name", 'password', "location", "location_other", "country", )}),
        ('Recruiter Fields', {'fields': ("company", "funding_stage", "funding_amount", "is_recruiter")}),
        ('Candidate Fields', {'fields': ("resume", "tech_lang", 
        "tech_cloud", "property_type", "role_sought", "desired_salary_range", "remote_capable",  "desired_time", 'field_experience', 'proptech_experience', "is_candidate")}),
    )
    

admin.site.register(CustomUser, UserAdminConfig)
admin.site.unregister(Group)

