

from django.contrib import admin
from .models import (
    Profile,
    RegistrationForEvent,
)


admin.site.register(Profile)
admin.site.register(RegistrationForEvent)
