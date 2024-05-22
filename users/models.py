from django.db import models
from django.contrib.auth.models import AbstractUser,Group
# Create your models here.
# users/models.py

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

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    # Add additional fields for student profile
    enrollment_number = models.CharField(max_length=20)
    batch_year = models.IntegerField()
    semester = models.IntegerField()
    section = models.CharField(max_length=10)
    shift = models.CharField(max_length=10)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.username


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