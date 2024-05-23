from django.contrib import admin
from home.models import StudentAchievement, Experience, Education, Publication, Honors, Committee_membership, ResearchProject, Patent
# Register your models here.
admin.site.register(StudentAchievement)
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Publication)
admin.site.register(Honors)
admin.site.register(Committee_membership)
admin.site.register(ResearchProject)
admin.site.register(Patent)
