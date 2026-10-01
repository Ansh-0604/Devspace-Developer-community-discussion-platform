from django.contrib import admin
from .models import Blog,Profile,Project, DevLog

# Register your models here.

admin.site.register(Blog)
admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(DevLog)


