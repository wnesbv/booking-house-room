
from django.db import models
from django.conf import settings


class Appointment(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.DO_NOTHING
    )
    room_number = models.CharField(max_length=50)
    appointment_with = models.CharField(max_length=50, blank=True)

    date = models.DateTimeField(max_length=50)
    time_start = models.DateTimeField(max_length=50)
    time_end = models.CharField(max_length=50)

    update_time = models.DateTimeField(auto_now=True, auto_now_add=False)
    frist_time = models.DateTimeField(auto_now=False, auto_now_add=True)
    image = models.ImageField(default="agent.jpg", upload_to="agent_image\\")

    def __str__(self):
        return "Asentamiento: {} {} {} {} ".format(
            self.date, self.time_start, self.room_number, self.appointment_with
        )
