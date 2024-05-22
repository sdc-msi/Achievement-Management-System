from django.db import models
from django.contrib.auth.models import AbstractUser,Group
import datetime
# Create your models here.
# users/models.py

def current_year():
    return datetime.date.today().year

def year_choices():
    return [(r, r) for r in range(1980, current_year() + 1)]

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pics/', default='profile_pics/default.png')
    portfolio_links = models.URLField(max_length=200, blank=True)
    department = models.CharField(max_length=100, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    # Add any common fields here

    def __str__(self):
        return self.username
    
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"
    
faculty_group, created = Group.objects.get_or_create(name='faculty')
student_group, created = Group.objects.get_or_create(name='student')

class Faculty(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add additional fields for faculty profile
    employee_id = models.CharField(max_length=20, unique=True)
    shift = models.CharField(max_length=10)
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100,default='Computer Science')
    about = models.TextField(null=True, blank=True)
    expertise = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    contact_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    gender = models.CharField(null=True,blank=True, max_length=15)
    
    def __str__(self):
        return self.user.username

shift_type = [
    (1, 'Morning'),
    (2, 'Evening'),
]

course_types = [
    ('bca', 'Bachelor of Computer Applications'),
    ('bba', 'Bachelor of Business Administration'),
    ('mba', 'Masters of Business Administration'),
    ('bcom', 'Bachelor of Commerce'),
    ('bed', 'Bachelor of Education'),
    ('ballb', 'Bachelor of Law'),
    ('btech', 'Bachelor of Technology'),
]

sections = [
    ('a', 'A'),
    ('b', 'B'),
]

class Batch(models.Model):
    year = models.IntegerField(choices=year_choices(), default=current_year)
    section = models.CharField(max_length=5, choices=sections, default='a')
    shift = models.IntegerField(choices=shift_type, default='1')
    course = models.CharField(max_length=50, choices=course_types, default='bca')
    assigned_to = models.ForeignKey(Faculty, on_delete=models.PROTECT, blank=True, null=True)

    def __str__(self):
        return f"{self.course.upper()} {self.year}, Section {self.section.upper()}, Shift {self.shift}"


    def assigned_to_name(self):
        return self.assigned_to.user.first_name +" "+  self.assigned_to.user.last_name
    
    def batch_shift(self):
        if self.shift==1:
            return "Morning"
        elif self.shift==2:
            return "Evening"
        else:
            return"Invalid batch"

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add additional fields for student profile
    enrollment_number = models.CharField(max_length=20)
    batch = models.ForeignKey(Batch, on_delete=models.PROTECT, null=True, blank=True)
    course = models.CharField(max_length=100,default='bca')
    batch_year = models.IntegerField()
    semester = models.IntegerField()
    section = models.CharField(max_length=10)
    shift = models.CharField(max_length=10)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


