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

from time import timezone

def add_publication(request):
    if (request.method == 'POST'):
        faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
        title = request.POST.get('title')
        work_type = request.POST.get('work-type')
        title = request.POST.get('title')
        journal_name = request.POST.get('journal-title')
        year = request.POST.get('year')
        authors = request.POST.get('author')
        doi = request.POST.get('doi')
        issuing_organization = request.POST.get('issue_org')
        issue_date = request.POST.get('issue_date')
        url = request.POST.get('url')
        volume = request.POST.get('volume')
        page_number = request.POST.get('page-no')
        publisher_name = request.POST.get('publisher')
        file = request.FILES['pub_file']
        print(issuing_organization,title)

        values = {'title': title,
                'work_type': work_type,
                'journal_name': journal_name,
                'year': year, 
                'authors': authors, 
                'doi':doi, 
                'issuing_organization': issuing_organization,
                'issue_date': issue_date,
                'url': url,
                'volumee': volume,
                'page_number': page_number, 
                'publisher_name': publisher_name,
                'file': file }

        for key, value in values.items():
            print(f"{key}: {value}")

        publication = Publication(
            faculty=request.user.faculty,
            work_type=work_type,
            title=title,
            journal_name=journal_name,
            year=year,
            authors=authors,
            doi=doi,
            issuing_organization=issuing_organization,
            issue_date=issue_date,
            url=url,
            volume=volume,
            page_number=page_number,
            publisher_name=publisher_name,
            file=file,
        )
        publication.save()
        print("Data Saved Successfully : ",publication.title)

        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))

def add_about(request):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    

    if request.method == 'POST':
        about = request.POST.get('about')
        print(about)
        faculty.about = about
        faculty.save()
        print("About section added: ",faculty.about)
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))

    
def add_expertise(request):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)

    if request.method == 'POST':
        exp = request.POST.get('expertise')
        print(exp)
        faculty.expertise = exp
        faculty.save()
        print("expertise section added: ",faculty.expertise)
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))




def add_email(request):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)

    if request.method == 'POST':
        email = request.POST.get('email')
        faculty.user.email = email
        faculty.user.save()
        print("Faculty Email Added")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))

def add_personal_info(request):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    if request.method == 'POST':
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        faculty.dob = dob
        faculty.gender = gender
        faculty.save()
        print("Personal Data Saved successfully")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))






def add_contact_info(request):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    if request.method == 'POST':
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        faculty.address = address
        faculty.contact_number = contact
        faculty.save()
        print("Contact Info Saved successfully")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))





# edit profile views





def edit_experience(request,pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    experience = get_object_or_404(Experience,faculty=faculty, pk=pk)
    if request.method == 'POST':
        experience.title = request.POST['designation']
        experience.department = request.POST['department']
        experience. employment_type = request.POST['organisation']
        experience.company_name = request.POST['institute']
        experience.location = request.POST['location']
        experience.start_date = request.POST['startdate']
        experience.end_date = request.POST['enddate']
        experience.description = request.POST['description']

        print("edit experience done : ",experience.title)
        experience.save()
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))
    

def edit_education(request,  pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    education = get_object_or_404(Education, faculty=faculty, pk=pk)
    if request.method == 'POST':
        education.degree = request.POST.get('qualification')
        education.field_of_study = request.POST['field_of_study']
        education.school = request.POST.get('institute')
        education.start_date = request.POST['start_date']
        education.end_date = request.POST['end_date']
        education.grade = request.POST['grade']
        education.save()
        print("Edit education done : ", education.degree)
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))


def edit_honor(request, pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    honor = get_object_or_404(Honors, faculty=faculty, pk=pk)
    if request.method == 'POST':
        title = request.POST['title']
        organization = request.POST['issuing_organization']
        issue_year = request.POST['year']
        description = request.POST['description']
        
        honor.title = title
        honor.issuing_organization = organization
        honor.issue_year = issue_year
        honor.description = description
        honor.save()
        print("Edit education done : ", honor.title)
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))
    
def edit_doctoral_thesis(request, pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    thesis =  get_object_or_404(Doctoral_thesis, faculty=faculty, pk=pk)
    if request.method == 'POST':
        print(request.POST.get('researcher_names'))
        thesis.researchers_name = request.POST.get('researcher_names')
        print(thesis.researchers_name)
        thesis.title = request.POST.get('title')
        thesis.institute = request.POST.get('institute')
        thesis.awarded_year = request.POST.get('awarded_year')
        thesis.desc = request.POST.get('description')
        thesis.save()
        print(" Thesis Edit Done : ",thesis.title,thesis.researchers_name)
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))




def edit_committee_membership(request, pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    committee_membership = get_object_or_404(Committee_membership, pk=pk)
    if request.method == 'POST':
        committee_membership.organization = request.POST['organisation']
        committee_membership.designation = request.POST['designation']
        committee_membership.start_date = request.POST['startdate']
        committee_membership.end_date = request.POST['enddate']
        committee_membership.save()
        print("Commmittee Membership edit done : ",committee_membership.organization)
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))

def edit_research_projects(request,pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    projects = get_object_or_404(ResearchProject,pk=pk)
    if request.method == 'POST':
        projects.title = request.POST.get('project-title')
        projects.description = request.POST.get('description')
        projects.start_date = request.POST.get('start_date')
        projects.end_date = request.POST.get('end_date')
        projects.ongoing = request.POST.get('ongoing', False)
        projects.role = request.POST.get('role')
        projects.funding_agency = request.POST.get('funding-agency')
        projects.grant_number = request.POST.get('grant-no')
        projects.status = request.POST.get('status', "ongoing")
        projects.amount = request.POST.get('amount')

        projects.save()
        print(" Research project Edit Done : ",projects.title, projects.amount)
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))



def edit_patent(request,pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    patent = get_object_or_404(Patent, pk=pk)
    if request.method == 'POST':
        patent.title = request.POST.get('title')
        patent.inventors = request.POST.get('inventors')
        patent.application_number = request.POST.get('app-number')
        patent.patent_number = request.POST.get('patent-number')
        patent.filing_country = request.POST.get('filing-country')
        patent.subject_category = request.POST.get('subject-category')
        patent.filing_date = request.POST.get('filing-date')
        patent.publication_date = request.POST.get('publication-date')
        patent.status = request.POST.get('status', "pending")

        patent.save()
        print(" Patent Edit Done : ",patent.title)
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))

    
#delete views
def delete_experience(request, pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    experience = get_object_or_404(Experience, id=pk, faculty=request.user.faculty)

    if request.method == 'POST':
        experience.delete()
        print("Experience object deleted succesfully")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))

def delete_education(request,pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    education = get_object_or_404(Education, id=pk, faculty=request.user.faculty)

    if request.method == 'POST':
        education.delete()
        print("Education object deleted succesfully")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))

def delete_honors(request,pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    honor = get_object_or_404(Honors, id=pk, faculty=request.user.faculty)
    if request.method == 'POST':
        honor.delete()
        print("Honor/Award object deleted succesfully")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))


def delete_doctoral_thesis(request,pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    thesis = get_object_or_404(Doctoral_thesis, id=pk, faculty=request.user.faculty)
    if request.method == 'POST':
        thesis.delete()
        print("Doctoral Thesis object deleted succesfully")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))


def delete_committee_membership(request,pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    cm = get_object_or_404(Committee_membership, id=pk, faculty=request.user.faculty)
    if request.method == 'POST':
        cm.delete()
        print("Membership object deleted succesfully")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))
    

def delete_research_project(request,pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    rp = get_object_or_404(ResearchProject, id=pk, faculty=request.user.faculty)
    if request.method == 'POST':
        rp.delete()
        print("Research Project object deleted succesfully")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))
    

def delete_patent(request,pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    patent = get_object_or_404(Patent, id=pk, faculty=request.user.faculty)
    if request.method == 'POST':
        patent.delete()
        print("Research Project object deleted succesfully")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))
    


def dashboard(request):

    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)


    context = {
        "faculty": faculty,
        
    }

    return render(request, 'faculty/dashboard.html', context=context)


def batch_list(request):
    return render(request, 'faculty/batch-list.html')


def faculty_list(request):
    return render(request, 'faculty/faculty_list.html')