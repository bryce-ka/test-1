# Generated by Django 4.0.6 on 2022-09-06 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Company', '0002_alter_job_location_alter_job_remote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='role_sought',
            field=models.CharField(choices=[('C Suite', 'C Suite'), ('Data Engineering', 'Data Engineering'), ('Data Science', 'Data Science'), ('Engineering', 'Engineering'), ('Front End Engineer', 'Front End Engineer'), ('Product Management', 'Product Management'), ('Sales Entry', 'Sales Entry'), ('Sales Exec', 'Sales Exec'), ('Sales Mid-level', 'Sales Mid-level'), ('UX Designer', 'UX Designer'), ('Other', 'Other')], max_length=80),
        ),
    ]
