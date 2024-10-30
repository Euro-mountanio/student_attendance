# attendance/admin.py
from django.contrib import admin
from .models import Attendance, Student_record

admin.site.register(Attendance)
admin.site.register(Student_record)