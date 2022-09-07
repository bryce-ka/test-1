from django import forms
from .models import Skills



class NewSkillForm(forms.ModelForm):
    class Meta:
        model = Skills
        fields = ['skill']

    