from django.db import models
import datetime
from datetime import date

from users.models import *

def current_year():
    return datetime.date.today().year

def year_choices():
    return [(r, r) for r in range(1980, current_year() + 1)]

class StudentAchievement(models.Model):
    type_choices = (
        ('1', 'Academic'),
        ('2', 'Non-Academic'),
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, unique=False)
    event_name = models.CharField(max_length=255)
    achievement_type = models.CharField(max_length=255, choices=type_choices)
    category = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    date = models.DateField()
    title = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    file = models.ImageField(upload_to='achievement_files/')
    image_url = models.URLField()
    approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True, blank=True)
    is_pending = models.BooleanField(default=True)


class Experience(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=225) #designation
    department = models.CharField(max_length=225,default="Computer Applications")
    employment_type = models.CharField(max_length=100)#organization type
    company_name = models.CharField(max_length=225)#institution name
    location = models.CharField(max_length=225)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True, blank=True)
    is_pending = models.BooleanField(default=True)

    @property
    def end_date_display(self):
        if self.end_date > date.today():
            return "Present"
        return self.end_date

class Education(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='educations')
    school = models.CharField(max_length=225)
    degree = models.CharField(max_length=225)
    field_of_study = models.CharField(max_length=225)
    start_date = models.DateField() 
    end_date = models.DateField()
    grade = models.CharField(max_length=10)

class Honors(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='honors')
    title = models.CharField(max_length=225) #award name
    issuing_organization = models.CharField(max_length=225)
    issue_year = models.IntegerField(choices=year_choices(), default=current_year())
    description = models.TextField()
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True, blank=True, related_name='approving_faculty')
    is_pending = models.BooleanField(default=True)


class Committee_membership(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='committee_memberships')
    name = models.CharField(max_length=225) #name
    organization = models.CharField(max_length=225)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    @property
    def end_date_display(self):
        if self.end_date > date.today():
            return "Present"
        return self.end_date

class ResearchProject(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='research_projects')
    title = models.CharField(max_length=225)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    ongoing = models.BooleanField(default=False)
    role = models.CharField(max_length=225)
    funding_agency = models.CharField(max_length=225)
    grant_number = models.CharField(max_length=225)
    status = models.CharField(max_length=50,choices=[('completed', 'Completed'), ('ongoing', 'Ongoing')])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True, blank=True)
    is_pending = models.BooleanField(default=True)


class Patent(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='patents')
    title = models.CharField(max_length=225)
    inventors = models.CharField(max_length=225)
    application_number = models.CharField(max_length=225)
    patent_number = models.CharField(max_length=225)
    filing_country = models.CharField(max_length=225)
    subject_category = models.CharField(max_length=225)
    filing_date = models.DateField()
    publication_date = models.DateField()
    status = models.CharField(max_length=50, choices=[('pending', 'Pending'),('published','Published'), ('granted', 'Granted')])
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True, blank=True)
    is_pending = models.BooleanField(default=True)


work_type_choices = [
    ('article', 'Article'),
    ('article_in_press', 'Article in Press'),
    ('book', 'Book'),
    ('book_chapter', 'Book Chapter'),
    ('conference_paper', 'Conference Paper'),
    ('conference_proceedings', 'Conference Proceedings'),
    ('editorial', 'Editorial'),
    ('erratum', 'Erratum'),
    ('letter', 'Letter'),
    ('note', 'Note'),
    ('review', 'Review'),
    ('retracted_article', 'Retracted Article'),
    ('short_survey', 'Short Survey'),
    ('other', 'Other'),
]


class Publication(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='publications')
    work_type = models.CharField(max_length=225,choices=work_type_choices,default='article')
    title = models.CharField(max_length=225,default="unknown title")
    year = models.IntegerField(choices=year_choices(), default=current_year())
    journal_name = models.CharField(max_length=225,default="ABC Journal")
    authors = models.CharField(max_length=225,default=student.name)
    doi = models.CharField(max_length=225, null=True, blank=True)
    issuing_organization = models.CharField(max_length=225,default="Unknown Organization")
    issue_date = models.DateField()
    url = models.URLField(null=True,blank=True)
    volume = models.CharField(max_length=225,null=True,blank=True)
    page_number = models.CharField(max_length=225,null=True,blank=True)
    publisher_name = models.CharField(max_length=225,null=True,blank=True)
    file = models.FileField(upload_to='publications/')
    is_approved = models.BooleanField(default=False)
    approved_by = models.ForeignKey(Faculty, on_delete=models.PROTECT, null=True, blank=True)
    is_pending = models.BooleanField(default=True)
