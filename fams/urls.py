

from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = "fams"

urlpatterns = [
    path('faculty_list/', faculty_list, name="faculty_list"),
    path('profile/<int:faculty_id>/', faculty_profile, name="faculty_profile"),
    path('add_experience/',add_experience, name='add_experience'),
    path('add_education/', add_education, name='add_education'),
    path('add_honor/', add_honor, name='add_honor'),
    path('dashboard/', dashboard, name='dashboard'),
]