

from django.urls import path
from .import views

urlpatterns = [
    path("", views.agent, name="agent_home"),
    path("my_appointment/", views.agent, name="teacher_appointment"),
    path(
        "create_appointment/",
        views.agent_appointment_list,
        name="agent_appointment_list",
    ),
    path(
        "create_appointment/delete/<indicator>/",
        views.appointment_delete,
        name="appointment_delete",
    ),
    path(
        "create_appointment/update/<indicator>/",
        views.agent_update,
        name="agent_update",
    ),
]
