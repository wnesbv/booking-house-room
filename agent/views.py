
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from .models import Appointment
from .forms import AppointmentForm


def agent(request):
    group_name = Group.objects.all().filter(user=request.user)
    group_name = str(group_name[0])

    if group_name == "Agent":
        user_name = request.user.get_username()
        appointment_list = (
            Appointment.objects.all().order_by("-id").filter(user=request.user)
        )
        query = request.GET.get("q")
        if query:
            appointment_list = appointment_list.filter(
                appointment_with__icontains=query
            )
        appointments = {"query": appointment_list, "user_name": user_name}
    return render(request, "agent/agent.html", appointments)


def agent_appointment_list(request):
    group_name = Group.objects.all().filter(user=request.user)
    group_name = str(group_name[0])

    if group_name == "Agent":
        user_name = request.user.get_username()
        appointment_list = (
            Appointment.objects.all().order_by("-id").filter(user=request.user)
        )
        query = request.GET.get("q")
        if query:
            appointment_list = appointment_list.filter(date__icontains=query)

        appointments = {
            "query": appointment_list,
            "user_name": user_name,
            "form": AppointmentForm(),
        }
        form = AppointmentForm(request.POST or None)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.user = request.user
            saving.save()
            messages.success(request, "Post Created Sucessfully")
    return render(request, "agent/agent_create.html", appointments)


def appointment_delete(request, indicator):
    group_name = Group.objects.all().filter(user=request.user)
    group_name = str(group_name[0])

    if group_name == "Agent":
        single_appointment = Appointment.objects.get(id=indicator)
        single_appointment.delete()
        messages.success(request, "Your profile was updated.")
    return redirect("/agent/create_appointment/")


def agent_update(request, indicator):
    group_name = Group.objects.all().filter(user=request.user)
    group_name = str(group_name[0])
    if group_name == "Agent":
        user_name = request.user.get_username()
        appointment_list = (
            Appointment.objects.all().order_by("-id").filter(user=request.user)
        )
        query = request.GET.get("q")
        if query:
            appointment_list = appointment_list.filter(date__icontains=query)

        single_appointment = single_appointment = Appointment.objects.get(id=indicator)
        form = AppointmentForm(request.POST or None, instance=single_appointment)
        if form.is_valid():
            saving = form.save(commit=False)
            saving.user = request.user
            saving.save()
            messages.success(request, "Post Created Sucessfully")
            return redirect("/agent/create_appointment/")

        appointments = {
            "query": appointment_list,
            "user_name": user_name,
            "form": form,
        }

    return render(request, "agent/agent_update.html", appointments)
