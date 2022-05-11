

from django.contrib import admin
from .models import Appointment


class TeacherAdmin(admin.ModelAdmin):
    list_display = ["date", "time_start", "time_end", "room_number", "appointment_with"]
    list_filter = ("date", "update_time")

admin.site.register(Appointment, TeacherAdmin)
