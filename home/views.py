from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
# from .forms import StudentAchievementForm
from users.models import Student, Faculty, Batch
from home.models import Experience, Education, Patent, Publication, ResearchProject, Committee_membership, Honors
from .models import StudentAchievement
from users.decorators import group_required
from django.urls import reverse_lazy,reverse
from users.views import user_is_faculty
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Q
from django.db.models import Count

# Create your views here.
def home(request):
    print(request.user)
    print('home')
     # this shows user name in terminal when login is done
    print(request.user.username)
    print(user_is_faculty(request.user))
    return render(request, 'home/home.html', {'title': 'Home'})

def home_new(request):
    return render(request, 'home/home_new.html')

def search_student(request):
    
    batch_year = request.GET.get('batch_year', '')
    course = request.GET.get('course', '')
    shift = request.GET.get('shift', '')
    section = request.GET.get('section', '')
    print(shift,course,section,batch_year)
    if shift=="Morning":
        shift=1
    elif shift=="Evening":
        shift=2
    
    filters = Q()
    if batch_year:
        filters |= Q(batch__year=batch_year)
    if course:
        filters |= Q(batch__course=course)
    if shift:
        filters |= Q(batch__shift=shift)
    if section:
        filters |= Q(batch__section=section)
    

    if filters:
        
        print(filters)
        students = Student.objects.filter(filters)
    else:
        
        students = Student.objects.all()
        print(students)

    if not students:
        print("No Student found in this query")

    context = {
        "students": students,
        
        
    }
    
    return render(request, 'student/student-search.html',context=context)


# @group_required('student')
# def create_achievement(request):
    
#     if request.method == 'POST':
#         achievement_form = StudentAchievementForm(request.POST, request.FILES)
#         stu = Student.objects.get(user=request.user)
#         print(stu)
#         print(type(stu))
#         if achievement_form.is_valid():
#             achievement = achievement_form.save(commit=False)
#             achievement.student = stu
#             achievement.save()
#             messages.success(request, f'Your achievement has been submitted for approval!')
#             return HttpResponseRedirect(reverse('home:home'))

#     else:
#         achievement_form = StudentAchievementForm()

#     return render(request, 'home/create_achievement.html', { 'form': achievement_form })

@group_required('faculty')
def view_pending(request,pk):
    student = get_object_or_404(Student, id=pk)
    
    pending_honors = Honors.objects.filter(student=student, is_pending=True)
    pending_research_projects = ResearchProject.objects.filter(student=student, is_pending=True)
    pending_patents = Patent.objects.filter(student=student, is_pending=True)
    pending_publications = Publication.objects.filter(student=student, is_pending=True)
    
    print(pending_honors)
    context = {
        'student': student,
        'pending_honors': pending_honors,
        'pending_research_projects': pending_research_projects,
        'pending_patents': pending_patents,
        'pending_publications': pending_publications,
    }
    
    return render(request, 'home/pending_achievements.html',context=context)


# @group_required( 'student')
# def student_view_all(request):
#     achievements = StudentAchievement.objects.filter(approved=1)

#     return render(request, 'home/all_achievements.html', {'achievements': achievements,'student':True})

# @group_required('faculty')
# def faculty_view_all(request):
#     achievements = StudentAchievement.objects.all()
#     return render(request, 'home/all_achievements.html', {'achievements': achievements})




def approve_achievement(request, pk):
    achievement_type = request.POST.get('achievement_type')
    achievement_model = None
    print(achievement_type)
    if achievement_type == 'honor':
        achievement_model = Honors
    elif achievement_type == 'research_project':
        achievement_model = ResearchProject
    elif achievement_type == 'patent':
        achievement_model = Patent
    elif achievement_type == 'publication':
        achievement_model = Publication

    

    if achievement_model:
        achievement = get_object_or_404(achievement_model, id=pk)
        print(achievement.student.id)
        achievement.is_pending = False
        achievement.is_approved = True
        achievement.approved_by = request.user.faculty
        # print(request.user.faculty)
        achievement.save()
        messages.success(request, f'{achievement_type} achievement has been approved successfully.')
    # pass
    return HttpResponseRedirect(reverse('home:pending_achievements', kwargs={"pk": achievement.student.id}))




# @group_required('faculty')
# def toggle_approval(request, achievement_id):
#     print('toggle_approval')
#     achievement = get_object_or_404(StudentAchievement, id=achievement_id)
#     print(achievement)
#     print(achievement.approved) 
#     if request.method == 'POST':
#         print("HIHBUHVJBNKJBH")
#         # Get the approval status from the form submission
#         approval_status = request.POST.get('approval_status')
        

#         # Toggle the 'approved' field
#         achievement.approved = (approval_status == 'approved')


#         # Set the 'approved_by' field if approving
#         if achievement.approved:
#             achievement.approved_by = request.user.faculty 
            
#              # Replace with your actual user fetching logic
#         achievement.is_pending = 0
#         achievement.save()
#         return HttpResponseRedirect(reverse('home:achievement details',args=(achievement_id,)))


# def student_profile(request, student_id):
#     student = get_object_or_404(Student, id=student_id)
#     experiences = student.experiences.all().order_by("start_date")
#     educations = student.educations.all()
#     honors = student.honors.all()
#     committee_memberships = student.committee_memberships.all()
#     research_projects = student.research_projects.all()
#     patents = student.patents.all()
#     publications = student.publications.all()

#     education_string = list(educations.values_list('degree', flat=True))

#     is_own_profile = False

#     print(hasattr(request.user, 'student'))

#     if request.user.is_authenticated:
#         if hasattr(request.user, 'student'):
#             is_own_profile = request.user.student == student

#     print(f"is_own_profile = {is_own_profile}")

#     context = {
#         'student': student,
#         'experiences': experiences,
#         'educations': educations,
#         'education_string': education_string,
#         'honors': honors,
#         'committee_memberships': committee_memberships,
#         'research_projects': research_projects,
#         'patents': patents,
#         'publications': publications,
#         'is_own_profile': is_own_profile,
#     }
#     return render(request, 'student/profile.html',context)


def student_profile(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    experiences = student.experiences.all().order_by("start_date")
    educations = student.educations.all()
    honors = Honors.objects.filter(student=student)
    committee_memberships = student.committee_memberships.all()
    research_projects = ResearchProject.objects.filter(student=student)
    patents = Patent.objects.filter(student=student)
    publications = Publication.objects.filter(student=student)

    education_string = list(educations.values_list('degree', flat=True))

    is_own_profile = False

    if request.user.is_authenticated:
        if hasattr(request.user, 'student'):
            is_own_profile = request.user.student == student

    context = {
        'student': student,
        'experiences': experiences,
        'educations': educations,
        'education_string': education_string,
        'honors': honors,
        'committee_memberships': committee_memberships,
        'research_projects': research_projects,
        'patents': patents,
        'publications': publications,
        'is_own_profile': is_own_profile,
    }
    return render(request, 'student/profile.html', context)

def add_experience(request):
    if request.method == 'POST':
        # Get the logged-in user's faculty instance
        student = get_object_or_404(Student, id=request.user.student.id)
        
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
            student=student,
            title=title,
            department=department,
            employment_type=employment_type,
            company_name=company_name,
            location=location,
            start_date=start_date,
            end_date=end_date,
            description=description
        )

        # Redirect to the faculty profile page
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))



def add_education(request):
    if (request.method == 'POST'):
        student = get_object_or_404(Student, id=request.user.student.id)
        qualification = request.POST.get('qualification')
        field_of_study = request.POST.get('field_of_study')
        institute = request.POST.get('institute')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        grade = request.POST.get('grade')
        
        education = Education.objects.create(
            student=student,
            degree=qualification,
            school=institute,
            field_of_study=field_of_study,
            start_date=start_date,
            end_date=end_date,
            grade=grade
        )

        return HttpResponseRedirect(reverse('home:student_profile', kwargs={"student_id": student.id}))


# def add_honor(request):
#     if (request.method == 'POST'):
#         student = get_object_or_404(Student, id=request.user.student.id)
#         title = request.POST.get('title')
#         issuing_org = request.POST.get('issuing_organization')
#         year = request.POST.get('year')
#         desc = request.POST.get('description')

#         honor = Honors.objects.create(
#             student=student,
#             title=title,
#             issuing_organization=issuing_org,
#             issue_year=year,
#             description=desc
#         )

#         return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))


def add_honor(request):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=request.user.student.id)
        title = request.POST.get('title')
        issuing_org = request.POST.get('issuing_organization')
        year = request.POST.get('year')
        desc = request.POST.get('description')
        

        honor = Honors.objects.create(
            student=student,
            title=title,
            issuing_organization=issuing_org,
            issue_year=year,
            description=desc,
            achievement_type='2'  
        )

        return redirect(reverse('home:student_profile', kwargs={'student_id': student.id}))
    

def add_committee_membership(request):
    if request.method == 'POST':
        student = get_object_or_404(Student, id=request.user.student.id)
        designation = request.POST['designation'] # designation
        organization = request.POST['organisation']
        start_date = request.POST['startdate']
        end_date = request.POST['enddate']
        description = request.POST['designation']

        print("all data : ",designation,organization,start_date,end_date,description)
        committee_membership = Committee_membership.objects.create(
            student=student,
            name=designation,
            organization=organization,
            start_date=start_date,
            end_date=end_date,
            description=description
        )

        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))


def add_research_project(request):
    if (request.method == 'POST'):
        student = get_object_or_404(Student, id=request.user.student.id)
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
            student=student,
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

        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))


def add_patent(request):
    if (request.method == 'POST'):
        student = get_object_or_404(Student, id=request.user.student.id)
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
            student=student,
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

        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))

from time import timezone

def add_publication(request):
    if request.method == 'POST' and request.FILES['file']:

        student = get_object_or_404(Student, id=request.user.student.id)
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
            student=request.user.student,
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

        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))

def add_about(request):
    student = get_object_or_404(Student, id=request.user.student.id)

    if request.method == 'POST':
        about = request.POST.get('about')
        print(about)
        student.about = about
        student.save()
        print("About section added: ",student.about)
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))

    
def add_expertise(request):
    student = get_object_or_404(Student, id=request.user.student.id)

    if request.method == 'POST':
        exp = request.POST.get('expertise')
        print(exp)
        student.expertise = exp
        student.save()
        print("expertise section added: ",student.expertise)
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))




def add_email(request):
    student = get_object_or_404(Student, id=request.user.student.id)

    if request.method == 'POST':
        email = request.POST.get('email')
        student.user.email = email
        student.user.save()
        print("student Email Added")
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))

def add_personal_info(request):
    student = get_object_or_404(Student, id=request.user.student.id)
    if request.method == 'POST':
        dob = request.POST.get('dob')
        gender = request.POST.get('gender')
        student.dob = dob
        student.gender = gender
        student.save()
        print("Personal Data Saved successfully")
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))






def add_contact_info(request):
    student = get_object_or_404(Student, id=request.user.student.id)
    if request.method == 'POST':
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        student.address = address
        student.contact_number = contact
        student.save()
        print("Contact Info Saved successfully")
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))


# edit profile views

def edit_experience(request,pk):
    student = get_object_or_404(Student, id=request.user.student.id)
    experience = get_object_or_404(Experience,student=student, pk=pk)
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
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))
    

def edit_education(request,  pk):
    student = get_object_or_404(Student, id=request.user.student.id)
    education = get_object_or_404(Education, student=student, pk=pk)
    if request.method == 'POST':
        education.degree = request.POST.get('qualification')
        education.field_of_study = request.POST['field_of_study']
        education.school = request.POST.get('institute')
        education.start_date = request.POST['start_date']
        education.end_date = request.POST['end_date']
        education.grade = request.POST['grade']
        education.save()
        print("Edit education done : ", education.degree)
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))


def edit_honor(request, pk):
    student = get_object_or_404(Student, id=request.user.student.id)
    honor = get_object_or_404(Honors, student=student, pk=pk)
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
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))
    

def edit_committee_membership(request, pk):
    student = get_object_or_404(Student, id=request.user.student.id)
    committee_membership = get_object_or_404(Committee_membership, pk=pk)
    if request.method == 'POST':
        committee_membership.organization = request.POST['organisation']
        committee_membership.designation = request.POST['designation']
        committee_membership.start_date = request.POST['startdate']
        committee_membership.end_date = request.POST['enddate']
        committee_membership.save()
        print("Commmittee Membership edit done : ",committee_membership.organization)
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))

def edit_research_projects(request,pk):
    student = get_object_or_404(Student, id=request.user.student.id)
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
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))



def edit_patent(request,pk):
    student = get_object_or_404(Student, id=request.user.student.id)
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
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))
    

def edit_publication(request,pk):
    publication = get_object_or_404(Publication, id=pk, student=request.user.student)
    
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
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': request.user.student.id}))

    
#delete views
def delete_experience(request, pk):
    student = get_object_or_404(Student, id=request.user.student.id)
    experience = get_object_or_404(Experience, id=pk, student=request.user.student)

    if request.method == 'POST':
        experience.delete()
        print("Experience object deleted succesfully")
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))

def delete_education(request,pk):
    student = get_object_or_404(Student, id=request.user.student.id)
    education = get_object_or_404(Education, id=pk, student=request.user.student)

    if request.method == 'POST':
        education.delete()
        print("Education object deleted succesfully")
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))

def delete_honors(request,pk):
    student = get_object_or_404(Student, id=request.user.student.id)
    honor = get_object_or_404(Honors, id=pk, student=request.user.student)
    if request.method == 'POST':
        honor.delete()
        print("Honor/Award object deleted succesfully")
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))


def delete_committee_membership(request,pk):
    student = get_object_or_404(Student, id=request.user.student.id)
    cm = get_object_or_404(Committee_membership, id=pk, student=request.user.student)
    if request.method == 'POST':
        cm.delete()
        print("Membership object deleted succesfully")
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))
    

def delete_research_project(request,pk):
    student = get_object_or_404(Student, id=request.user.student.id)
    rp = get_object_or_404(ResearchProject, id=pk, student=request.user.student)
    if request.method == 'POST':
        rp.delete()
        print("Research Project object deleted succesfully")
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))
    

def delete_patent(request,pk):
    student = get_object_or_404(Student, id=request.user.student.id)
    patent = get_object_or_404(Patent, id=pk, student=request.user.student)
    if request.method == 'POST':
        patent.delete()
        print("Research Project object deleted succesfully")
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))
    

def delete_publication(request,pk):
    student = get_object_or_404(Student, id=request.user.student.id)
    publication = get_object_or_404(Publication, id=pk, student=request.user.student)
    if request.method == 'POST':
        publication.delete()
        print("Publication object deleted succesfully")
        return HttpResponseRedirect(reverse('home:student_profile', kwargs={'student_id': student.id}))


def dashboard(request):
    print("hoolalalala")

    student = get_object_or_404(Student, id=request.user.student.id)
    print(student)
    student_batch = Batch.objects.get(id=student.batch.id)
    assigned_faculty = Faculty.objects.get(id=student_batch.assigned_to.id)
    assigned_batches = Batch.objects.filter(id=student.batch.id).annotate(count = Count("student"))
    other_batches = Batch.objects.exclude(id=student.batch.id).annotate(count = Count("student"))
    other_faculties = Faculty.objects.all().exclude(id=assigned_faculty.id)[:5]
    print(other_faculties)
    
    print("Id: ", assigned_batches[0].id)
    print("Count: ", assigned_batches[0].count)

    context = {
        "student": student,
        "assigned_faculty": assigned_faculty,
        "assigned_batches" : assigned_batches,
        "other_batches" : other_batches,
        "other_faculties": other_faculties,
    }

    return render(request, 'student/dashboard.html', context=context)

def batch_list(request, batch_id):
    student = get_object_or_404(Student, id=request.user.student.id)
    batch = get_object_or_404(Batch, id=batch_id)
    print(batch)

    search_query = request.GET.get('search', '')
    if search_query:
        students = Student.objects.filter(batch=batch, user__first_name__icontains=search_query)
    else:
        students = Student.objects.filter(batch=batch)
    
    context ={
        "students":students,
        "batch":batch,
        "search_query" : search_query
    }   

    return render(request, 'student/batch-list.html',context=context)