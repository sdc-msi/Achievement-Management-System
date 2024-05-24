import io
from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, PageBreak
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from django.shortcuts import render
from users.models import Faculty, Batch, Student
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .models import Experience, Education, Honors, Doctoral_thesis, Professional_membership, Committee_membership, ResearchProject, Patent, Publication
from django.conf import settings
from django.db.models import Count
from home.models import Honors, ResearchProject, Patent, Publication

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

    is_own_profile = False

    if request.user.is_authenticated:
        if hasattr(request.user, 'faculty'):
            is_own_profile = request.user.faculty == faculty

    print(f"is_own_profile = {is_own_profile}")

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
        'is_own_profile': is_own_profile,
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
    if request.method == 'POST' and request.FILES['file']:

        faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
        title = request.POST.get('title')
        work_type = request.POST.get('work-type')
        title = request.POST.get('title')
        journal_name = request.POST.get('journal-title')
        year = request.POST.get('year')
        authors = request.POST.get('author')
        doi = request.POST.get('doi')
        issuing_organization = request.POST.get('io')
        issue_date = request.POST.get('issue_date')
        url = request.POST.get('url')
        volume = request.POST.get('volume')
        page_number = request.POST.get('page-no')
        publisher_name = request.POST.get('publisher')
        file = request.FILES['file']
        

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
    

def edit_publication(request,pk):
    publication = get_object_or_404(Publication, id=pk, faculty=request.user.faculty)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        work_type = request.POST.get('work-type')
        journal_name = request.POST.get('journal-title')
        year = request.POST.get('year')
        authors = request.POST.get('author')
        doi = request.POST.get('doi')
        issuing_organization = request.POST.get('io')
        issue_date = request.POST.get('issue_date')
        url = request.POST.get('url')
        volume = request.POST.get('volume')
        page_number = request.POST.get('page-no')
        publisher_name = request.POST.get('publisher')

        publication.title = title
        publication.work_type = work_type
        publication.journal_name = journal_name
        publication.year = year
        publication.authors = authors
        publication.doi = doi
        publication.issuing_organization = issuing_organization
        publication.issue_date = issue_date
        publication.url = url
        publication.volume = volume
        publication.page_number = page_number
        publication.publisher_name = publisher_name

        if 'file' in request.FILES:
            publication.file = request.FILES['file']

        publication.save()
        print("Publication object edited successfully")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': request.user.faculty.id}))

    
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
    

def delete_publication(request,pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    publication = get_object_or_404(Publication, id=pk, faculty=request.user.faculty)
    if request.method == 'POST':
        publication.delete()
        print("Publication object deleted succesfully")
        return HttpResponseRedirect(reverse('fams:faculty_profile', kwargs={'faculty_id': faculty.id}))

@login_required(login_url="/users/facultyLogin/")
def dashboard(request):
    print("hoolalalala")

    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    print(faculty)
    assigned_batches = Batch.objects.filter(assigned_to=faculty).annotate(count = Count("student"))
    other_batches = Batch.objects.exclude(assigned_to=faculty).annotate(count = Count("student"))
    other_faculties = Faculty.objects.all().exclude(id=faculty.id)
    print(other_faculties)

    students = Student.objects.filter(batch=assigned_batches[1])
    # print(students)
    
    
    pending_honors_count = Honors.objects.filter( is_pending=True).count()
    pending_research_projects_count = ResearchProject.objects.filter( is_pending=True).count()
    pending_patents_count = Patent.objects.filter( is_pending=True).count()
    pending_publications_count = Publication.objects.filter( is_pending=True).count()

    total_pending_count = (pending_honors_count + pending_research_projects_count +
                            pending_patents_count + pending_publications_count)
    print("Total Pending Count: ", total_pending_count)

    print("Id: ", assigned_batches[0].id)
    print("Count: ", assigned_batches[0].count)

    context = {
        "faculty": faculty,
        "assigned_batches" : assigned_batches,
        "other_batches" : other_batches,
        "other_faculties": other_faculties,
        "total_pending_count": total_pending_count,
    }

    return render(request, 'faculty/dashboard.html', context=context)

@login_required(login_url="/users/facultyLogin/")
def batch_list(request,pk):
    faculty = get_object_or_404(Faculty, id=request.user.faculty.id)
    batch = get_object_or_404(Batch,assigned_to=faculty,id=pk)
    print(batch)



    search_query = request.GET.get('search', '')
    if search_query:
        students = Student.objects.filter(batch=batch, user__first_name__icontains=search_query)
    else:
        students = Student.objects.filter(batch=batch)

    students_with_pending_counts = []

    for student in students:
        pending_honors_count = Honors.objects.filter(student=student, is_pending=True).count()
        pending_research_projects_count = ResearchProject.objects.filter(student=student, is_pending=True).count()
        pending_patents_count = Patent.objects.filter(student=student, is_pending=True).count()
        pending_publications_count = Publication.objects.filter(student=student, is_pending=True).count()

        total_pending_count = (pending_honors_count + pending_research_projects_count +
                               pending_patents_count + pending_publications_count)

        students_with_pending_counts.append({
            'student': student,
            'pending_count': total_pending_count
        })
    
    
    context ={
        "students":students,
        "batch":batch,
        "search_query" : search_query,
        "students_with_pending_counts": students_with_pending_counts,
    }   

    return render(request, 'faculty/batch-list.html',context=context)


def faculty_list(request):
    faculties = Faculty.objects.all()

    print(faculties.values())

    context = {
        'faculties': faculties,
    }

    return render(request, 'faculty/faculty_list.html', context=context)



stylesheet = getSampleStyleSheet()

h1 = stylesheet['Heading1']
h2 = stylesheet['Heading2']
h3 = stylesheet['Heading3']
italic = stylesheet['Italic']
bodytext = stylesheet['BodyText']

def createParagraph(flowable, text, style):
    flowable.append(Paragraph(text, style))

def addSpacer(flowable, height):
    flowable.append(Spacer(10, height))

def pageBreak(flowable):
    flowable.append(PageBreak())

def faculty_download_pdf(request, faculty_id):

    faculty = get_object_or_404(Faculty, id=faculty_id)

    buffer = io.BytesIO()
    my_doc = SimpleDocTemplate(buffer, pagesize=A4)
    sample_style_sheet = getSampleStyleSheet()

    flowables = []
        

    experiences = faculty.experiences.all().order_by("start_date")
    educations = faculty.educations.all()
    honors = faculty.honors.all()
    doctoral_theses = faculty.doctoral_theses.all()
    professional_memberships = faculty.professional_memberships.all()
    committee_memberships = faculty.committee_memberships.all()
    research_projects = faculty.research_projects.all()
    patents = faculty.patents.all()
    publications = faculty.publications.all()

    createParagraph(flowables, faculty.user.get_full_name(), h1)
    createParagraph(flowables, faculty.about, bodytext)

    createParagraph(
        flowables,
        str(faculty.designation) + ", " + str(faculty.department),
        italic
    )
    
    # if (experiences):
    #     createParagraph(flowables, "Experience", h2)
    #     for exp in experiences:
    #         flowables.append(Paragraph(
    #             str(exp.title) + " at " + str(exp.company_name),
    #             h3 
    #         ))
    #         flowables.append(Paragraph('Department: ' + str(exp.department), sample_style_sheet['Italic']))
    #         flowables.append(Paragraph(
    #             str(exp.start_date) + " - " + str(exp.end_date),
    #             sample_style_sheet['Italic']
    #         ))
    
    #     addSpacer(flowables, 15)

    # if (educations):
    #     createParagraph(flowables, "Education", h2)
    #     for edu in educations:
    #         createParagraph(flowables, str(edu.school), h3)
    #         createParagraph(flowables, f"{edu.degree}, {edu.field_of_study}", italic)
    #         createParagraph(flowables,
    #             str(edu.start_date) + " - " + str(edu.end_date),
    #             italic
    #         )
        
    #     addSpacer(flowables, 15)

    if honors:
        createParagraph(flowables, "Honors", h2)
        for hons in honors:
            createParagraph(flowables, str(hons.title), h3)
            createParagraph(flowables, hons.issuing_organization, italic)
            createParagraph(flowables,
                str(hons.issue_year),
                italic
            )
        
        addSpacer(flowables, 15)


    if doctoral_theses:
        createParagraph(flowables, "Doctoral Theses", h2)
        for thesis in doctoral_theses:
            createParagraph(flowables, thesis.title, h3)
            createParagraph(flowables, thesis.researchers_name, italic)
            createParagraph(flowables, thesis.institute, italic)
            createParagraph(flowables, str(thesis.awarded_year), italic)
        
        addSpacer(flowables, 15)
    
    if professional_memberships:
        createParagraph(flowables, "Professional Membership", h2)
        for membership in professional_memberships:
            createParagraph(flowables, membership.title, h3)
            createParagraph(flowables, membership.organization, italic)
            createParagraph(flowables, membership.member_type, italic)
            createParagraph(flowables,
                str(membership.start_date) + " - " + str(membership.end_date),
                italic
            )

        addSpacer(flowables, 15)
    
    if committee_memberships:
        createParagraph(flowables, "Committee Membership", h2)
        for membership in committee_memberships:
            createParagraph(flowables, membership.name, h3)
            createParagraph(flowables, membership.organization, italic)
            createParagraph(flowables,
                str(membership.start_date) + " - " + str(membership.end_date),
                italic
            )

        addSpacer(flowables, 15)
    
    if research_projects:
        createParagraph(flowables, "Research Projects", h2)
        for project in research_projects:
            createParagraph(flowables, project.title, h3)
            createParagraph(flowables, project.role, italic)
            createParagraph(flowables,
                str(project.start_date) + " - " + str(project.end_date),
                italic
            )
            createParagraph(flowables, f"Rs. {project.amount} granted by {str(project.funding_agency)}", italic)

        addSpacer(flowables, 15) 

    if patents:
        createParagraph(flowables, "Patents", h2)
        for patent in patents:
            createParagraph(flowables, patent.title, h3)
            createParagraph(flowables, patent.inventors, italic)
            createParagraph(flowables, f"Status: {patent.status}", italic)
            if patent.status == 'completed':
                createParagraph(flowables, str(patent.filing_date), italic)

        addSpacer(flowables, 15)

    if publications:
        createParagraph(flowables, "Publications", h2)
        for pub in publications:
            createParagraph(flowables, pub.title, h3)
            createParagraph(flowables, pub.work_type.replace('_', " ").title(), italic)
            createParagraph(flowables, f"{pub.journal_name}, {str(pub.issue_date)}", italic)
            createParagraph(flowables, pub.authors, italic)

    # pageBreak(flowables)

    my_doc.build(flowables)
    pdf_value = buffer.getvalue()
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{faculty.user.get_full_name()} AMS report.pdf"'

    response.write(buffer.getvalue())
    buffer.close()
    return response
