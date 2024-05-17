from django.shortcuts import render
from users.models import Faculty
from django.shortcuts import get_object_or_404
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

    context = {
        'faculty': faculty,
        'experiences': experiences,
        'educations': educations,
        'honors': honors,
        'doctoral_theses': doctoral_theses,
        'professional_memberships': professional_memberships,
        'committee_memberships': committee_memberships,
        'research_projects': research_projects,
        'patents': patents,
        'publications': publications,
    }
    return render(request, 'faculty/profile.html',context)

