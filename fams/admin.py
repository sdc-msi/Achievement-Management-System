from django.contrib import admin

# Register your models here.
from .models import Experience, Education, Publication

admin.site.register(Experience)
admin.site.register(Education)
admin.site.register(Publication)

