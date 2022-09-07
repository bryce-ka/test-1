import django_filters 
from Company.models import Job


class OrderFilter(django_filters.FilterSet):
    class Meta:
        model = Job
        fields = ['department', 'location', 'languages', 'cloud','property_type', 'role_sought', 'role_sought_other', 'salary_range', 'remote', 'funding_stage', 'funding_amount', 'job_type' ]
        