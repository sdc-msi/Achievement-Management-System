

from django.contrib import admin
from django.urls import path, include
from .views import *

app_name = "fams"

urlpatterns = [
    path('faculty_list/', faculty_list, name="faculty list"),
    path('profile', faculty_profile, name="faculty profile"),
]