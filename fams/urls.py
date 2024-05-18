

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
    path('add_doctoral_thesis/', add_doctoral_thesis, name='add_doctoral_thesis'),
    path('add_research_project/', add_research_project, name='add_research_project'),
    path('dashboard/', dashboard, name='dashboard'),
    path('batch_list/', batch_list, name='batch_list'),
]