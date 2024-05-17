from django.contrib import admin

# Register your models here.
from .models import *
admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Publication)
admin.site.register(Honors)
admin.site.register(Doctoral_thesis)
admin.site.register(Professional_membership)
admin.site.register(Committee_membership)
admin.site.register(ResearchProject)
admin.site.register(Patent)

