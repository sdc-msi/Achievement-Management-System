from django.shortcuts import render
from users.models import Faculty
# Create your views here.
def faculty_list(request):
    faculties = Faculty.objects.select_related('user').all()
    return render(request, 'home/faculty_list.html',{'faculties':faculties})


def faculty_profile(request):
    return render(request, 'faculty/profile.html')
