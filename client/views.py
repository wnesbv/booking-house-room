

from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from agent.models import Appointment


def quick_appointmnet(request):
    group_name = Group.objects.all().filter(user=request.user)
    group_name = str(group_name[0])

    if group_name == "Client":
        user_name = request.user.get_username()
        appointment_list = Appointment.objects.all().order_by("-user")
        query = request.GET.get("q")
        if query:
            appointment_list = appointment_list.filter(
                user__first_name__icontains=query
            )

        appointments = {"query": appointment_list, "user_name": user_name}
    return render(request, "client/client_quick_appointmnet.html", appointments)


def client(request):
    group_name = Group.objects.all().filter(user=request.user)
    group_name = str(group_name[0])

    if group_name == "Client":
        user_name = request.user.get_username()
        appointment_list = (
            Appointment.objects.all().order_by("-id").filter(appointment_with=user_name)
        )
        query = request.GET.get("q")
        if query:
            appointment_list = appointment_list.filter(
                user__first_name__icontains=query
            )

        appointments = {
            "query": appointment_list,
            "user_name": user_name,
        }
    return render(request, "client/client.html", appointments)


def appointment_book(request, indicator):
    group_name = Group.objects.all().filter(user=request.user)
    group_name = str(group_name[0])

    if group_name == "Client":
        user_name = request.user.get_username()
        single_appointment = Appointment.objects.get(id=indicator)
        form = single_appointment
        form.appointment_with = user_name
        form.save()

    return redirect("client")
