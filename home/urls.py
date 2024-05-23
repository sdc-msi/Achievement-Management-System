# sams/urls.py

from django.contrib import admin
from django.urls import path, include
from .views import *
#import url


app_name = "home"

urlpatterns = [
    path('',home_new,name="home"),
    path('search-student/',search_student,name="search_student"),
    # path('',home,name="home"),
    # path('new_achievement/', create_achievement, name="create achievement"),
    path('pendingAchievements/<int:pk>/', view_pending, name="pending_achievements"),
    path('approve_achievement/<int:pk>/', approve_achievement, name = 'approve_achievement'),
    # path('achievementDetails/<int:achievement_id>/', view_details, name='achievement details'),
    # path('for_f_achievements/', faculty_view_all, name="faculty_achievments_view"),
    # path('for_f_pending/', view_pending, name='pending_achievements'),
    # path('for_s_achievements/', student_view_all, name="student_achievments_view"),
    # path('toggle_approval/<int:achievement_id>/', toggle_approval, name='toggle_approval'),
    path('profile/<int:student_id>/', student_profile, name='student_profile'),
    path('add_about/', add_about, name='add_about'),
    path('add_expertise/', add_expertise , name='add_expertise'),
    path('add_email/', add_email, name='add_email'),
    path('add_personal_info/', add_personal_info, name='add_personal_info'),
    path('add_contact_info/', add_contact_info, name='add_contact_info'),
    path('add_experience/',add_experience, name='add_experience'),
    path('add_education/', add_education, name='add_education'),
    path('add_honor/', add_honor, name='add_honor'),
    path('add_research_project/', add_research_project, name='add_research_project'),
    path('add_patent/', add_patent, name='add_patent'),
    path('add_publication/', add_publication, name='add_publication'),
    path('add_committee_membership/',add_committee_membership, name='add_committee_membership'),
    path('add_publication/', add_publication, name='add_publication'),
    path('edit_experience/<int:pk>/', edit_experience, name='edit_experience'),
    path('edit_education/<int:pk>/', edit_education, name='edit_education'),
    path('edit_honor/<int:pk>/', edit_honor, name='edit_honor'),
    path('edit_committee_membership/<int:pk>/', edit_committee_membership, name='edit_committee_membership'),
    path('edit_research_projects/<int:pk>/', edit_research_projects, name='edit_research_projects'),
    path('edit_patent/<int:pk>/', edit_patent, name='edit_patent'),
    path('edit_publication/<int:pk>/', edit_publication, name='edit_publication'),
    path('delete_experience/<int:pk>',delete_experience, name='delete_experience'),
    path('delete_education/<int:pk>',delete_education, name='delete_education'),
    path('delete_honors/<int:pk>',delete_honors, name='delete_honors'),
    path('delete_committee_membership/<int:pk>', delete_committee_membership, name='delete_committee_membership'),
    path('delete_research_project/<int:pk>', delete_research_project, name='delete_research_project'),
    path('delete_patent/<int:pk>', delete_patent, name='delete_patent'),
    path('delete_publication/<int:pk>', delete_publication, name='delete_publication'),
    path('dashboard/', dashboard, name='dashboard'),
    path('batch_list/<int:batch_id>', batch_list, name='batch_list'),
    # Add other app URLs here
]
