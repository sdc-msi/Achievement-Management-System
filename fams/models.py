from django.db import models

from users.models import Faculty

class Experience(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=225)
    employment_type = models.CharField(max_length=100)
    company_name = models.CharField(max_length=225)
    location = models.CharField(max_length=225)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

class Education(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='educations')
    school = models.CharField(max_length=225)
    degree = models.CharField(max_length=225)
    field_of_study = models.CharField(max_length=225)
    start_date = models.DateField() 
    end_date = models.DateField()
    grade = models.CharField(max_length=10)

class Publication(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='publications')
    name = models.CharField(max_length=225)
    issuing_organization = models.CharField(max_length=225)
    issue_date = models.DateField()
    expiration_date = models.DateField()
    credential_id = models.CharField(max_length=225)
    credential_url = models.URLField()
    file = models.FileField(upload_to='publications/')