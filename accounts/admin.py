from django.contrib import admin
from . models import Department, Subject, Student, Teacher

# Register your models here.
admin.site.register(Department)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Teacher)