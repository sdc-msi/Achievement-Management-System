from django.shortcuts import render
from users.models import Faculty
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Experience, Education, Honors, Doctoral_thesis, Professional_membership, Committee_membership, ResearchProject, Patent, Publication
from django.conf import settings

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


def add_committee_membership(request):
    if request.method == 'POST':
        faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
        designation = request.POST['designation'] # designation
        organization = request.POST['organisation']
        start_date = request.POST['startdate']
        end_date = request.POST['enddate']
        description = request.POST['designation']

        print("all data : ",designation,organization,start_date,end_date,description)
        committee_membership = Committee_membership.objects.create(
            faculty=faculty,
            name=designation,
            organization=organization,
            start_date=start_date,
            end_date=end_date,
            description=description
        )

        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))


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
    if (request.method == 'POST'):
        faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
        title = request.POST.get('title')
        inventors = request.POST.get('inventors')
        application_no = request.POST.get('app-number')
        patent_no = request.POST.get('patent-number')
        filing_country = request.POST.get('filing-country')
        subject_category = request.POST.get('subject-category')
        filing_date = request.POST.get('filing-date')
        publication_date = request.POST.get('publication-date')
        status = request.POST.get('status', "pending")

        patent = Patent.objects.create(
            faculty=faculty,
            title=title,
            inventors=inventors,
            application_number=application_no,
            patent_number=patent_no,
            filing_country=filing_country,
            subject_category=subject_category,
            filing_date=filing_date,
            publication_date=publication_date,
            status=status,
        )

        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))

# Method to handle uploaded file for add_publication
# def handle_uploaded_publication(file):
#     print("===============")
#     print(settings.MEDIA_ROOT+file.name)
#     print("===============")
#     filepath = "publications/" + file.name()
#     with open(settings.MEDIA_ROOT + filepath, "wb+") as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)

def add_publication(request):
    if (request.method == 'POST'):
        faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
        title = request.POST.get('title')
        work_type = request.POST.get('work-type')
        journal_name = request.POST.get('journal-title')
        year = request.POST.get('year')
        authors = request.POST.get('author')
        issue_date = request.POST.get('issue_date')
        issue_org = request.POST.get('issue_org')
        url = request.POST.get('url')
        doi = request.POST.get('doi')
        volume = request.POST.get('volume')
        page_number = request.POST.get('page-no')
        publisher_name = request.POST.get('publisher')
        file = request.FILES.get('pub_file')

        print("===============")
        for key, val in request.FILES.items():
            print(f"{key}: {val}")
            print("===============")

        # handle_uploaded_publication(file)
        # handle_uploaded_file(file)
        
        # publication = Publication.objects.create(
        #     faculty=faculty,
        #     work_type=work_type,
        #     title=title,
        #     year=year,
        #     journal_name=journal_name,
        #     authors=authors,
        #     doi=doi,
        #     issuing_organization=issue_org,
        #     issue_date=issue_date,
        #     url=url,
        #     volume=volume,
        #     page_number=page_number,
        #     publisher_name=publisher_name
        #     file=file # IMPLEMENT THIS
        # )

        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))


def dashboard(request):
    return render(request, 'faculty/dashboard.html')


def batch_list(request):
    return render(request, 'faculty/batch-list.html')