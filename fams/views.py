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
    experiences = faculty.experiences.all().order_by("start_date")
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


# def add_experience(request):
#      print("csdhbvmndakfhjbcndkjfknsv,mkcvjkds cnjkvbdn")
#      if request.method == 'POST':
#         print("HEHEHEHE")
#         #faculty id is id of current logged in user
#         faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
#         title = request.POST['designation']
#         department = request.POST['department']
#         employment_type = request.POST['organisation']
#         company_name = request.POST['institute']
#         location = request.POST['location']
#         start_date = request.POST['startdate']
#         end_date = request.POST['enddate']
#         description = request.POST['description']

#         print("all data",faculty,title,department,employment_type,company_name,location,start_date,end_date,description)

#         experience = Experience.objects.create(
#             faculty=faculty,
#             title=title,
#             department=department,
#             employment_type=employment_type,
#             company_name=company_name,
#             location=location,
#             start_date=start_date,
#             end_date=end_date,
#             description=description
#         )

#         return HttpResponseRedirect(reverse('fams:faculty_profile',kwargs={'faculty_id': faculty}))  

from django.shortcuts import get_object_or_404

def add_experience(request):
    if request.method == 'POST':
        # Get the logged-in user's faculty instance
        faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
        
        title = request.POST['designation']
        department = request.POST['department']
        employment_type = request.POST['organisation']
        company_name = request.POST['institute']
        location = request.POST['location']
        start_date = request.POST['startdate']
        end_date = request.POST['enddate']
        description = request.POST['description']



        # Create the Experience instance
        experience = Experience.objects.create(
            faculty=faculty,
            title=title,
            employment_type=employment_type,
            company_name=company_name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            description=description
        )

        # Redirect to the faculty profile page
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))



def add_education(request):
    if (request.method == 'POST'):
        faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
        qualification = request.POST.get('qualification')
        field_of_study = request.POST.get('field_of_study')
        institute = request.POST.get('institute')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        grade = request.POST.get('grade')
        
        education = Education.objects.create(
            faculty=faculty,
            degree=qualification,
            school=institute,
            field_of_study=field_of_study,
            start_date=start_date,
            end_date=end_date,
            grade=grade
        )

        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={"faculty_id": faculty.id}))


def add_honor(request):
    if (request.method == 'POST'):
        faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
        title = request.POST.get('title')
        issuing_org = request.POST.get('issuing_organization')
        year = request.POST.get('year')
        desc = request.POST.get('description')

        honor = Honors.objects.create(
            faculty=faculty,
            title=title,
            issuing_organization=issuing_org,
            issue_year=year,
            description=desc
        )

        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))

def add_doctoral_thesis(request):
    if (request.method == 'POST'):
        faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
        researcher_names = request.POST.get('researcher_names')
        title = request.POST.get('title')
        institute = request.POST.get('institute')
        awarded_year = request.POST.get('awarded_year')
        desc = request.POST.get('description')

        doctoral_thesis = Doctoral_thesis.objects.create(
            faculty=faculty,
            researchers_name=researcher_names,
            title=title,
            institute=institute,
            description=desc,
            awarded_year=awarded_year
        )

        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))

def add_professional_membership(request):
    pass


def add_committee_membership(request):
    pass


def add_research_project(request):
    if (request.method == 'POST'):
        faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
        title = request.POST.get('project-title')
        desc = request.POST.get('description')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        ongoing = request.POST.get('ongoing', False)
        role = request.POST.get('role')
        funding_agency = request.POST.get('funding-agency')
        grant_no = request.POST.get('grant-no')
        status = request.POST.get('status', "ongoing")
        amount = request.POST.get('amount')

        print(ongoing)
        research_project = ResearchProject.objects.create(
            faculty=faculty,
            title=title,
            description=desc,
            start_date=start_date,
            end_date=end_date,
            ongoing=ongoing,
            role=role,
            funding_agency=funding_agency,
            grant_number=grant_no,
            status=status,
            amount=amount
        )

        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))


def add_patent(request):
    pass


def add_publication(request):
    pass


def dashboard(request):
    return render(request, 'faculty/dashboard.html')


def batch_list(request):
    return render(request, 'faculty/batch-list.html')