from django.contrib import admin

# Register your models here.
from attendance.models import Child, Adult, Staff, Attendance_History

admin.site.register(Child)
admin.site.register(Adult)
admin.site.register(Staff)
admin.site.register(Attendance_History)