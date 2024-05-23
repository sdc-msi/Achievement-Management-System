from django.contrib import admin
from home.models import StudentAchievement, Experience, Education, Publication, Honors, Committee_membership, ResearchProject, Patent
# Register your models here.


@admin.register(Honors)
class HonorsAdmin(admin.ModelAdmin):
    list_display = ('student', 'achievement_type', 'title', 'issuing_organization', 'issue_year', 'date', 'is_approved', 'is_pending')
    list_filter = ('is_approved', 'is_pending')

@admin.register(ResearchProject)
class ResearchProjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'achievement_type', 'title', 'role', 'funding_agency', 'status', 'amount', 'ongoing', 'date', 'is_approved', 'is_pending')
    list_filter = ('is_approved', 'is_pending')

@admin.register(Patent)
class PatentAdmin(admin.ModelAdmin):
    list_display = ('student', 'achievement_type', 'title', 'inventors', 'application_number', 'patent_number', 'filing_country', 'subject_category', 'filing_date', 'publication_date', 'status', 'is_approved', 'is_pending')
    list_filter = ('is_approved', 'is_pending')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'achievement_type', 'title', 'work_type', 'journal_name', 'authors', 'doi', 'issuing_organization', 'issue_date', 'volume', 'page_number', 'publisher_name', 'url', 'date', 'is_approved', 'is_pending')
    list_filter = ('is_approved', 'is_pending')