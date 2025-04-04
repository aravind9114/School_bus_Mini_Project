from django.contrib import admin
from .models import User, Student,Attendance,DriverAttendance

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Attendance)
admin.site.register(DriverAttendance)