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
    path('new_achievement/', create_achievement, name="create achievement"),
    path('pendingAchievements/', view_pending, name="pending achievements"),
    path('achievementDetails/<int:achievement_id>/', view_details, name='achievement details'),
    path('for_f_achievements/', faculty_view_all, name="faculty_achievments_view"),
    path('for_f_pending/', view_pending, name='pending_achievements'),
    path('for_s_achievements/', student_view_all, name="student_achievments_view"),
    path('toggle_approval/<int:achievement_id>/', toggle_approval, name='toggle_approval'),
    path('profile/<int:student_id>/', student_profile, name='student_profile')
    # Add other app URLs here
]
