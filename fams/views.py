from django.shortcuts import render

# Create your views here.
def faculty_list(request):
    return render(request, 'home/faculty_list.html',)


def faculty_profile(request):
    return render(request, 'faculty/profile.html')