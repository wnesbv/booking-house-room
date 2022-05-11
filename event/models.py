

from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(default="First Name", max_length=30)
    last_name = models.CharField(default="Last Name", max_length=30)
    gender = models.CharField(
        default="my gender doesn't matter",
        choices=(
            ("male", "male"),
            ("female", "female"),
            ("my gender doesn't matter", "my gender doesn't matter"),
        ),
        max_length=50,
    )
    location = models.CharField(default="by minsk", max_length=30)
    age = models.CharField(default="101", max_length=3)
    image = models.ImageField(default="default.jpg", upload_to="profile_image")

    def __str__(self):
        return self.user.username


class RegistrationForEvent(models.Model):
    First_Name = models.CharField(max_length=30)
    Last_Name = models.CharField(max_length=30)
    gender = (models.CharField(max_length=50),)
    location = models.CharField(max_length=30)
    age = models.CharField(max_length=3)
    timestamp = models.DateTimeField(default=now)
