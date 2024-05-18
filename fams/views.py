from django.shortcuts import render
from users.models import Faculty
from django.shortcuts import get_object_or_404

from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Experience, Education, Honors, Doctoral_thesis, Professional_membership, Committee_membership, ResearchProject, Patent, Publication
# Create your views here.
def faculty_list(request):
    faculties = Faculty.objects.select_related('user').all()
    return render(request, 'home/faculty_list.html',{'faculties':faculties})


def faculty_profile(request,faculty_id):

    faculty = get_object_or_404(Faculty, id=faculty_id)
    experiences = faculty.experiences.all()
    educations = faculty.educations.all()
    honors = faculty.honors.all()
    doctoral_theses = faculty.doctoral_theses.all()
    professional_memberships = faculty.professional_memberships.all()
    committee_memberships = faculty.committee_memberships.all()
    research_projects = faculty.research_projects.all()
    patents = faculty.patents.all()
    publications = faculty.publications.all()

    education_string = list(educations.values_list('degree', flat=True))

    context = {
        'faculty': faculty,
        'experiences': experiences,
        'educations': educations,
        'education_string': education_string,
        'honors': honors,
        'doctoral_theses': doctoral_theses,
        'professional_memberships': professional_memberships,
        'committee_memberships': committee_memberships,
        'research_projects': research_projects,
        'patents': patents,
        'publications': publications,
    }
    return render(request, 'faculty/profile.html',context)


def add_experience(request):
     print("csdhbvmndakfhjbcndkjfknsv,mkcvjkds cnjkvbdn")
     if request.method == 'POST':
        print("HEHEHEHE")
        #faculty id is id of current logged in user
        faculty = request.user.faculty.id
        title = request.POST['designation']
        department = request.POST['department']
        employment_type = request.POST['organisation']
        company_name = request.POST['institute']
        location = request.POST['location']
        start_date = request.POST['startdate']
        end_date = request.POST['enddate']
        description = request.POST['description']

        print("all data",faculty,title,department,employment_type,company_name,location,start_date,end_date,description)
        return HttpResponseRedirect(reverse('faculty_profile',faculty_id=request.user.faculty.id))  


def add_education(request):
    pass


def add_honor(request):
    pass


def add_doctoral_thesis(request):
    pass


def add_professional_membership(request):
    pass


def add_committee_membership(request):
    pass


def add_research_project(request):
    pass


def add_patent(request):
    pass


def add_publication(request):
    pass


