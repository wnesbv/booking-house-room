
from datetime import date
from datetime import datetime
from django.utils.timezone import localtime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.views.generic import ListView, DetailView

from .forms import *
from .models import *


# def home(request):
#     context = {"rest_list_view": RestComplex.objects.all()}
#     return render(
#         request=request, template_name="restcomplex/home.html", context=context,
 #   )
class HomeRestListView(ListView):
    model = RestComplex
    paginate_by = 2
    context_object_name = "rest_list_view"
    template_name = "restcomplex/home.html"

    def get_queryset(self):
        user = self.request.user
        queryset = RestComplex.objects.all()
        return queryset


class RestListView(ListView):
    model = RestComplex
    template_name = "restcomplex/gallery_filter.html"
    context_object_name = "rest_list_view"


class RestDetailView(DetailView):
    model = RestComplex
    template_name = "restcomplex/rest_details.html"


def fitness(request):
    return render(request=request, template_name="restcomplex/fitness.html")


def index(request):
    user = request.user
    if user.username:
        if request.method == "POST":
            form = ReservationForm(request.POST)
            if form.is_valid():
                start_date = form.cleaned_data["start_date"]
                end_date = form.cleaned_data["end_date"]

                if start_date > end_date or start_date <= localtime():
                    messages.warning(request, "Please Enter Proper dates")
                    return redirect("index_rest")

                n_n = PreReservationRest()
                n_n.start_date = start_date
                n_n.end_date = end_date
                n_n.save()
                return redirect("book_rest", n_n.id)
            else:
                for e in form.errors:
                    messages.error(request, e)
                return redirect("index_rest")
        else:
            form = ReservationForm(request.POST)
            return render(request, "restcomplex/restcomplex_index.html", {"form": form})
    else:
        messages.warning(request, "You are not logged in. Please login")
        return redirect("home_rest")


def book(request, t):
    user = request.user
    if user.username:
        if request.method == "POST":
            return redirect("index_rest")
        else:
            e_s = PreReservationRest.objects.get(id=t)
            start_date = e_s.start_date
            end_date = e_s.end_date

            n_n = (
                ReservationRest.objects.filter(
                    Q(start_date__range=(start_date, end_date))
                    | Q(end_date__range=(start_date, end_date))
                )
                .filter(status=True)
                .filter(waiting=False)
            )

            R = []
            for b_a in n_n:
                f = b_a.rooms_allocated
                if f.id not in R:
                    R.append(f.id)
            gh_all = RestComplex.objects.all()
            context = []

            for g in gh_all:
                rooms_available = KindOfRest.objects.exclude(pk__in=R).filter(
                    recreation_id=g.id
                )
                no_rooms = 0
                rooms = []

                for b_a in rooms_available:

                    r_st = b_a.functionality_kor
                    functionality_kor = r_st
                    r_st = b_a.img_logo
                    img_logo = r_st
                    r_st = b_a.name
                    name = r_st
                    r_st = b_a.slug
                    slug = r_st
                    r_st = b_a.image
                    image = r_st
                    r_st = b_a.image_2
                    image_2 = r_st
                    r_st = b_a.image_3
                    image_3 = r_st
                    r_st = b_a.image_4
                    image_4 = r_st
                    r_st = b_a.image_5
                    image_5 = r_st
                    r_st = b_a.image_6
                    image_6 = r_st

                    r_st = b_a.hede
                    hede = r_st
                    r_st = b_a.hede_2
                    hede_2 = r_st
                    r_st = b_a.hede_3
                    hede_3 = r_st
                    r_st = b_a.hede_4
                    hede_4 = r_st
                    r_st = b_a.hede_5
                    hede_5 = r_st
                    r_st = b_a.hede_6
                    hede_6 = r_st

                    r_st = b_a.expe
                    expe = r_st
                    r_st = b_a.expe_2
                    expe_2 = r_st
                    r_st = b_a.expe_3
                    expe_3 = r_st
                    r_st = b_a.expe_4
                    expe_4 = r_st
                    r_st = b_a.expe_5
                    expe_5 = r_st
                    r_st = b_a.expe_6
                    expe_6 = r_st

                    r_st = b_a.disc
                    disc = r_st
                    r_st = b_a.disc_2
                    disc_2 = r_st
                    r_st = b_a.disc_3
                    disc_3 = r_st
                    r_st = b_a.disc_4
                    disc_4 = r_st
                    r_st = b_a.disc_5
                    disc_5 = r_st
                    r_st = b_a.disc_6
                    disc_6 = r_st

                for b_a in rooms_available:
                    r_st = b_a.rest_type
                    flag = 0
                    no_rooms = no_rooms + 1
                    for i in rooms:
                        if r_st in i.values():
                            i["count"] = i["count"] + 1
                            flag = 1

                    if flag == 0:
                        rooms.append(
                            {
                                "functionality_kor": functionality_kor,
                                "img_logo": img_logo,
                                "slug": slug,
                                "image": image,
                                "hede": hede,
                                "expe": expe,
                                "disc": disc,
                                "image_2": image_2,
                                "hede_2": hede_2,
                                "expe_2": expe_2,
                                "disc_2": disc_2,
                                "image_3": image_3,
                                "hede_3": hede_3,
                                "expe_3": expe_3,
                                "disc_3": disc_3,
                                "image_4": image_4,
                                "hede_4": hede_4,
                                "expe_4": expe_4,
                                "disc_4": disc_4,
                                "image_5": image_5,
                                "hede_5": hede_5,
                                "expe_5": expe_5,
                                "disc_5": disc_5,
                                "image_6": image_6,
                                "hede_6": hede_6,
                                "expe_6": expe_6,
                                "disc_6": disc_6,
                                "type": r_st,
                                "count": 1,
                                "name": name,
                            }
                        )
                context.append(
                    {
                        "gh_all": g,
                        "no_rooms": no_rooms,
                        "rooms": rooms,
                        "functionality_kor": functionality_kor,
                        "img_logo": img_logo,
                        "slug": slug,
                        "name": name,
                        "image": image,
                        "hede": hede,
                        "expe": expe,
                        "disc": disc,
                        "image_2": image_2,
                        "hede_2": hede_2,
                        "expe_2": expe_2,
                        "disc_2": disc_2,
                        "image_3": image_3,
                        "hede_3": hede_3,
                        "expe_3": expe_3,
                        "disc_3": disc_3,
                        "image_4": image_4,
                        "hede_4": hede_4,
                        "expe_4": expe_4,
                        "disc_4": disc_4,
                        "image_5": image_5,
                        "hede_5": hede_5,
                        "expe_5": expe_5,
                        "disc_5": disc_5,
                        "image_6": image_6,
                        "hede_6": hede_6,
                        "expe_6": expe_6,
                        "disc_6": disc_6,
                    }
                )
            return render(
                request, "fitness/available.html", {"rooms": context, "n_n": e_s}
            )
    else:
        messages.warning(request, "You are not logged in. Please login")
        redirect("home_rest")


def query(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]

            if start_date > end_date or start_date <= localtime():
                messages.warning(request, "Please Enter Proper dates")
                return redirect("home_rest")

            n_n = ReservationRest.objects.filter(
                Q(start_date__range=(start_date, end_date))
                | Q(end_date__range=(start_date, end_date))
            )

            R = []
            for b_a in n_n:
                f = b_a.rooms_allocated
                for g in f:
                    if g.id not in R:
                        R.append(g.id)
            gh_all = RestComplex.objects.all()
            context = []

            for g in gh_all:
                rooms_available = KindOfRest.objects.exclude(pk__in=R).filter(
                    recreation_id=g.id
                )
                no_rooms = 0
                rooms = []

                for b_a in rooms_available:

                    r_st = b_a.functionality_kor
                    functionality_kor = r_st
                    r_st = b_a.img_logo
                    img_logo = r_st
                    r_st = b_a.name
                    name = r_st
                    r_st = b_a.slug
                    slug = r_st
                    r_st = b_a.image
                    image = r_st
                    r_st = b_a.image_2
                    image_2 = r_st
                    r_st = b_a.image_3
                    image_3 = r_st
                    r_st = b_a.image_4
                    image_4 = r_st
                    r_st = b_a.image_5
                    image_5 = r_st

                for b_a in rooms_available:
                    r_st = b_a.rest_type
                    flag = 0
                    for i in rooms:
                        if r_st in i.values():
                            i["count"] = i["count"] + 1
                            flag = 1
                        no_rooms = no_rooms + 1
                    if flag == 0:
                        rooms.append(
                            {
                                "functionality_kor": functionality_kor,
                                "img_logo": img_logo,
                                "slug": slug,
                                "image": image,
                                "image_2": image_2,
                                "image_3": image_3,
                                "image_4": image_4,
                                "image_5": image_5,
                                "type": r_st,
                                "count": 1,
                                "name": name,
                            }
                        )

                context.append(
                    {
                        "gh_all": g,
                        "no_rooms": no_rooms,
                        "rooms": rooms,
                        "functionality_kor": functionality_kor,
                        "img_logo": img_logo,
                        "slug": slug,
                        "image": image,
                        "image_2": image_2,
                        "image_3": image_3,
                        "image_4": image_4,
                        "image_5": image_5,
                        "name": name,
                    }
                )
            return render(request, "fitness/available.html", {"rooms": context})
        else:
            messages.warning(request, "Requested Page Not Found ")
            return redirect("home_rest")
    else:
        form = ReservationForm(request.POST)
        return render(request, "fitness/something.html", {"form": form})


def book_rest_verify(request, g, t, rtype):
    user = request.user
    if user.username:
        if request.method == "POST":
            t = PreReservationRest.objects.get(id=t)
            t.recreation = RestComplex.objects.get(id=g)
            t.save()

            start_date = t.start_date
            end_date = t.end_date

            n_n = (
                ReservationRest.objects.filter(
                    Q(start_date__range=(start_date, end_date))
                    | Q(end_date__range=(start_date, end_date))
                )
                .filter(status=True)
                .filter(waiting=False)
            )

            R = []

            for d in n_n:
                f = d.rooms_allocated
                if f.id not in R:
                    R.append(f.id)
            R = KindOfRest.objects.filter(recreation=t.recreation).filter(
                rest_type=rtype
            )

            rooms = []
            for really in n_n:
                rooms.append(really.rooms_allocated)

            for rd in R:
                if rd not in rooms:
                    xyz = rd
                    break

            newreservation = ReservationRest()
            newreservation.bookingID = (
                str(xyz.roomID) + str(user.username) + str(datetime.date.today())
            )
            newreservation.start_date = start_date
            newreservation.end_date = end_date
            newreservation.user_booked = user
            newreservation.booktime = datetime.date.today()
            newreservation.recreation = t.recreation
            newreservation.status = True
            newreservation.rest_type = rtype
            newreservation.rooms_allocated = xyz
            newreservation.save()
            newpayment = PaymentRest()
            newpayment.paymentID = str(newreservation.bookingID) + str(
                xyz.price * (0.2)
            )
            newpayment.amount = xyz.price * 0.2
            newpayment.reservation = newreservation
            newpayment.user_booked = user
            newpayment.payment_time = datetime.date.today()
            newpayment.save()

            return render(
                request, "fitness/book_successful.html", {"reservation": newreservation}
            )
        else:
            messages.warning(request, "Requested Page Not Found ")
            # return redirect('home')
            return redirect("index_rest")
    else:
        messages.warning(request, "You are not logged in. Please login")
        return redirect("home_rest")


def cancel(request, id):
    user = request.user
    if user.username:

        reservation = ReservationRest.objects.get(id=id)
        reservation.status = False
        reservation.save()
        flag = 0

        for waiting_one in WaitingOnRest.objects.all():
            start_date = waiting_one.start_date
            end_date = waiting_one.end_date
            res_3 = waiting_one.resID

            n_n = (
                ReservationRest.objects.filter(
                    Q(start_date__range=(start_date, end_date))
                    | Q(end_date__range=(start_date, end_date))
                )
                .filter(status=True)
                .filter(waiting=False)
                .filter(rest_type=res_3.rest_type)
                .filter(recreation=res_3.recreation)
            )

            R = KindOfRest.objects.filter(recreation=res_3.recreation).filter(
                rest_type=res_3.rest_type
            )

            rooms = []
            for really in n_n:
                f = really.rooms_allocated
                if f not in rooms:
                    rooms.append(f)

            for rest_of in R:
                if rest_of not in rooms:
                    xyz = rest_of
                    flag = 1

                    res_3.rooms_allocated = xyz
                    res_3.waiting = False
                    res_3.save()
                    waiting_one.delete()
                    break

            if flag == 1:
                break

        newrefund = RefundRest()
        newrefund.refundID = str(reservation.bookingID) + str(user.username)
        newrefund.reservation = reservation
        newrefund.amount = reservation.rooms_allocated.price * (0.2)
        newrefund.user_booked = user
        newrefund.refund_time = datetime.date.today()
        payments = reservation.payments.all()

        for p in payments:
            res = p.reservation
            if res.id == id:
                newrefund.payment = p

        newrefund.save()
        messages.warning(
            request,
            "Your Booking with Booking number  "
            + str(reservation.bookingID)
            + " is cancelled Succesfully",
        )
        return render(
            request, "fitness/cancel_successful.html", {"reservation": reservation}
        )
    else:
        messages.warning(request, "you are not logged in or have no access")
        return redirect("login")


def my_bookings(request):
    user = request.user
    if user.username:
        n_n = (
            ReservationRest.objects.filter(user_booked=user)
            .order_by("-booktime")
            .filter(status=True)
        )
        bookings = []

        for t in n_n:
            g = t.recreation

            r_st = t.rooms_allocated
            bookings.append({"n_n": t, "gh_all": g, "R": r_st})
        context = {"bookings": bookings, "reservation": n_n}
        return render(request, "fitness/my_bookings.html", context)
    else:
        messages.warning(
            request, "You are not authorized to acces the requested page. Please Login "
        )
        return redirect("home_rest")


def waiting_show(request, t):
    user = request.user
    if user.username:
        if request.method == "POST":
            return redirect("index_rest")
        else:
            e_s = PreReservationRest.objects.get(id=t)
            start_date = e_s.start_date
            end_date = e_s.end_date

            gh_all = RestComplex.objects.all()
            context = []

            for g in gh_all:
                new_waiting = (
                    ReservationRest.objects.filter(
                        Q(start_date__range=(start_date, end_date))
                        | Q(end_date__range=(start_date, end_date))
                    )
                    .filter(status=True)
                    .filter(recreation=g)
                )

                rooms = []
                for b_a in new_waiting:
                    R = b_a.rest_type
                    flag = 0

                    for i in rooms:
                        if R in i.values():
                            i["count"] = i["count"] + 1
                            flag = 1

                    if flag == 0:
                        rooms.append({"type": R, "count": 1})

                context.append({"gh_all": g, "room2": rooms})
            return render(
                request, "fitness/waiting_show.html", {"rooms": context, "n_n": e_s}
            )
    else:
        messages.warning(request, "You are not logged in. Please login")
        redirect("home_rest")


def waiting(request, g, t, rtype):
    user = request.user
    if user.username:
        if request.method == "POST":
            t = PreReservationRest.objects.get(id=t)
            t.recreation = RestComplex.objects.get(id=g)
            t.save()

            newreservation = ReservationRest()
            newreservation.bookingID = str(t.recreation.code) + str(t.id)
            newreservation.start_date = t.start_date
            newreservation.end_date = t.end_date
            newreservation.user_booked = user
            newreservation.rest_type = rtype
            newreservation.booktime = datetime.date.today()
            newreservation.recreation = t.recreation
            newreservation.status = True
            newreservation.waiting = True
            newreservation.save()

            R = KindOfRest.objects.filter(recreation=t.recreation).filter(
                rest_type=rtype
            )

            newpayment = PaymentRest()
            newpayment.paymentID = str(newreservation.bookingID) + str(
                R[0].price * (0.2)
            )
            newpayment.amount = R[0].price * (0.2)
            newpayment.reservation = newreservation
            newpayment.user_booked = user
            newpayment.payment_time = datetime.date.today()
            newpayment.save()
            newwaiting = WaitingOnRest()
            newwaiting.resID = newreservation
            newwaiting.date_booked = newreservation.booktime
            newwaiting.start_date = newreservation.start_date
            newwaiting.end_date = newreservation.end_date
            newwaiting.save()

            return render(
                request,
                "fitness/waiting_successful.html",
                {
                    "reservation": newreservation,
                    "waiting": newwaiting,
                    "payment": newpayment,
                },
            )
        else:
            messages.warning(request, "Requested Page Not Found ")
            return redirect("index_rest")
    else:
        messages.warning(request, "You are not logged in. Please login")
        return redirect("home_rest")


def feedback(request):
    user = request.user
    if user.username:
        if request.method == "POST":
            form = FeedbackFormRest(request.POST)
            if form.is_valid():
                feed = form.cleaned_data.get("feed")
                newfeedback = FeedbackRest()
                newfeedback.user_of = user
                newfeedback.time = date.today()
                newfeedback.feed = feed
                newfeedback.feedbackID = (
                    str(user.username) + str(date.today()) + str(user.email)
                )
                newfeedback.save()
                return render(request, "fitness/feedback_successful.html")
            else:
                messages.error(request, "Invalid form details")
        form = FeedbackFormRest()
        return render(request, "fitness/feedback.html", context={"form": form})
    else:
        messages.warning(request, "You are not logged in. Please login")
        redirect("home_rest")


def cancelwaiting(request, id):
    user = request.user
    if user.username:

        reservation = ReservationRest.objects.get(id=id)
        reservation.status = False
        reservation.save()
        newrefund = RefundRest()
        newrefund.refundID = str(reservation.bookingID) + str(user.username)
        newrefund.reservation = reservation
        newrefund.user_booked = user
        newrefund.refund_time = datetime.date.today()

        payments = reservation.payments.all()

        for p in payments:
            res = p.reservation
            if res.id == id:
                newrefund.payment = p
                newrefund.amount = p.amount

        messages.warning(
            request,
            "Your Booking with Booking number  "
            + str(reservation.bookingID)
            + " is cancelled Succesfully",
        )
        return render(
            request, "fitness/cancel_successful.html", {"reservation": reservation}
        )
    else:
        messages.warning(request, "you are not logged in or have no access")
        return redirect("login")


def roomdetails(request, *args, **kwargs):
    user = request.user
    if user.username:
        offers = get_object_or_404(KindOfRest, slug=kwargs.get("slug"))

    context = {"offers": offers}
    return render(request, "fitness/roomdetails.html", context)


def rc_details(request, *args, **kwargs):
    user = request.user
    if user.username:
        restdetails = get_object_or_404(RestComplex, slug=kwargs.get("slug"))

    context = {"restdetails": restdetails}
    return render(request, "restcomplex/rest_details.html", context)
