

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
    path('add_patent/', add_patent, name='add_patent'),
    path('add_committee_membership/',add_committee_membership, name='add_committee_membership'),
    path('add_publication/', add_publication, name='add_publication'),
    path('dashboard/', dashboard, name='dashboard'),
    path('batch_list/', batch_list, name='batch_list'),
    path('edit_experience/<int:pk>/', edit_experience, name='edit_experience'),
    path('edit_education/<int:pk>/', edit_education, name='edit_education'),
    path('edit_honor/<int:pk>/', edit_honor, name='edit_honor'),
    path('edit_doctoral_thesis/<int:pk>/', edit_doctoral_thesis, name='edit_doctoral_thesis'),
    path('edit_committee_membership/<int:pk>/', edit_committee_membership, name='edit_committee_membership'),
    path('edit_research_projects/<int:pk>/', edit_research_projects, name='edit_research_projects'),
    path('edit_patent/<int:pk>/', edit_patent, name='edit_patent'),
    
]