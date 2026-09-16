from django.contrib import admin

from .models import Project, User, Note, Teacher


admin.site.register(Project)
admin.site.register(User)
admin.site.register(Note)
admin.site.register(Teacher)