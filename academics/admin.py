from django.contrib import admin

from .models import Project, User, Note, Teacher, Institution


admin.site.register(Project)
admin.site.register(User)
admin.site.register(Note)
admin.site.register(Teacher)
admin.site.register(Institution)