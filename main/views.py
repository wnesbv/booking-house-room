from datetime import date
from datetime import datetime
from django.utils.timezone import localtime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from main.forms import ReservationForm, FeedbackForm
from main.models import (
    PreReservation,
    Reservation,
    GuestHouse,
    Rooms,
    Payment,
    Refund,
    Feedback,
    WaitingOn,
)


def index(request):
    user = request.user
    if user.username:
        if request.method == "POST":
            form = ReservationForm(request.POST)

            if form.is_valid():
                start_date = form.cleaned_data["start_date"]
                end_date = form.cleaned_data["end_date"]
                # ...
                number_rooms = form.cleaned_data["number_rooms"]
                number_children = form.cleaned_data["number_children"]
                number_adults = form.cleaned_data["number_adults"]

                if start_date > end_date or start_date <= localtime():
                    messages.warning(request, "Please Enter Proper dates")
                    return redirect("index")

                n_n = PreReservation()
                n_n.start_date = start_date
                n_n.end_date = end_date
                # ...
                n_n.number_rooms_pre = number_rooms
                n_n.number_children_pre = number_children
                n_n.number_adults_pre = number_adults

                n_n.save()
                return redirect("book", n_n.id)

            else:
                for e in form.errors:
                    messages.error(request, e)
                return redirect("index")
        else:
            form = ReservationForm(request.POST)
            return render(request, "main/main_index.html", {"form": form})
    else:
        messages.warning(request, "You are not logged in. Please login")
        return redirect("login")


def book(request, t):
    user = request.user
    if user.username:
        if request.method == "POST":
            return redirect("index")
        else:
            e_s = PreReservation.objects.get(id=t)
            start_date = e_s.start_date
            end_date = e_s.end_date
            # ...
            number_rooms = e_s.number_rooms
            number_children = e_s.number_children
            number_adults = e_s.number_adults

            n_n = (
                Reservation.objects.filter(
                    Q(start_date__range=(start_date, end_date))
                    | Q(end_date__range=(start_date, end_date))
                )
                .filter(status=True)
                .filter(waiting=False)
                .filter(
                    number_rooms=number_rooms,
                    number_children=number_children,
                    number_adults=number_adults,
                )
            )

            gh_r = []
            for b_a in n_n:
                f = b_a.rooms_allocated
                if f.id not in gh_r:
                    gh_r.append(f.id)
            gh_all = GuestHouse.objects.all()
            context = []

            for g in gh_all:
                rooms_available = Rooms.objects.exclude(pk__in=gh_r).filter(
                    guesthouse_id=g.id
                )
                no_rooms = 0
                rooms = []

                for b_a in rooms_available:

                    r_m = b_a.functionality_rm
                    functionality_rm = r_m
                    r_m = b_a.img_logo
                    img_logo = r_m
                    r_m = b_a.name
                    name = r_m
                    r_m = b_a.slug
                    slug = r_m
                    r_m = b_a.image
                    image = r_m
                    r_m = b_a.image_2
                    image_2 = r_m
                    r_m = b_a.image_3
                    image_3 = r_m
                    r_m = b_a.image_4
                    image_4 = r_m
                    r_m = b_a.image_5
                    image_5 = r_m

                for b_a in rooms_available:
                    r_m = b_a.room_type
                    flag = 0
                    no_rooms = no_rooms + 1
                    for i in rooms:
                        if r_m in i.values():
                            i["count"] = i["count"] + 1
                            flag = 1

                    if flag == 0:
                        rooms.append(
                            {
                                "functionality_rm": functionality_rm,
                                "img_logo": img_logo,
                                "slug": slug,
                                "image": image,
                                "image_2": image_2,
                                "image_3": image_3,
                                "image_4": image_4,
                                "image_5": image_5,
                                "type": r_m,
                                "count": 1,
                                "name": name,
                            }
                        )
                context.append(
                    {
                        "gh_all": g,
                        "no_rooms": no_rooms,
                        "rooms": rooms,
                        "functionality_rm": functionality_rm,
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
            return render(
                request, "main/available.html", {"rooms": context, "n_n": e_s}
            )
    else:
        messages.warning(request, "You are not logged in. Please login")
        redirect("login")


def query(request):
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data["start_date"]
            end_date = form.cleaned_data["end_date"]
            # ...
            number_rooms = form.cleaned_data["number_rooms"]
            number_children = form.cleaned_data["number_children"]
            number_adults = form.cleaned_data["number_adults"]

            if start_date > end_date or start_date <= localtime():
                messages.warning(request, "Please Enter Proper dates")
                return redirect("index")

            n_n = Reservation.objects.filter(
                Q(start_date__range=(start_date, end_date))
                | Q(end_date__range=(start_date, end_date))
            ).filter(
                number_rooms=number_rooms,
                number_children=number_children,
                number_adults=number_adults,
            )

            gh_r = []
            for b_a in n_n:
                f = b_a.rooms_allocated
                for g in f:
                    if g.id not in gh_r:
                        gh_r.append(g.id)
            gh_all = GuestHouse.objects.all()
            context = []

            for g in gh_all:
                rooms_available = Rooms.objects.exclude(pk__in=gh_r).filter(
                    guesthouse_id=g.id
                )
                no_rooms = 0
                rooms = []

                for b_a in rooms_available:

                    r_m = b_a.functionality_rm
                    functionality_rm = r_m
                    r_m = b_a.img_logo
                    img_logo = r_m
                    r_m = b_a.name
                    name = r_m
                    r_m = b_a.slug
                    slug = r_m
                    r_m = b_a.image
                    image = r_m
                    r_m = b_a.image_2
                    image_2 = r_m
                    r_m = b_a.image_3
                    image_3 = r_m
                    r_m = b_a.image_4
                    image_4 = r_m
                    r_m = b_a.image_5
                    image_5 = r_m

                for b_a in rooms_available:
                    r_m = b_a.room_type
                    flag = 0
                    for i in rooms:
                        if r_m in i.values():
                            i["count"] = i["count"] + 1
                            flag = 1
                        no_rooms = no_rooms + 1
                    if flag == 0:
                        rooms.append(
                            {
                                "functionality_rm": functionality_rm,
                                "img_logo": img_logo,
                                "slug": slug,
                                "image": image,
                                "image_2": image_2,
                                "image_3": image_3,
                                "image_4": image_4,
                                "image_5": image_5,
                                "type": r_m,
                                "count": 1,
                                "name": name,
                            }
                        )

                context.append(
                    {
                        "gh_all": g,
                        "no_rooms": no_rooms,
                        "rooms": rooms,
                        "functionality_rm": functionality_rm,
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
            return render(request, "main/available.html", {"rooms": context})
        else:
            messages.warning(request, "Requested Page Not Found")
            return redirect("index")
    else:
        form = ReservationForm(request.POST)
        return render(request, "main/something.html", {"form": form})


def book_room_verify(request, g, t, rtype):
    user = request.user
    if user.username:
        if request.method == "POST":
            t = PreReservation.objects.get(id=t)
            t.guesthouse = GuestHouse.objects.get(id=g)
            t.save()

            start_date = t.start_date
            end_date = t.end_date
            # ...
            number_rooms = t.number_rooms
            number_children = t.number_children
            number_adults = t.number_adults

            n_n = (
                Reservation.objects.filter(
                    Q(start_date__range=(start_date, end_date))
                    | Q(end_date__range=(start_date, end_date))
                )
                .filter(status=True)
                .filter(waiting=False)
                .filter(
                    number_rooms=number_rooms,
                    number_children=number_children,
                    number_adults=number_adults,
                )
            )

            gh_r = []

            for d in n_n:
                f = d.rooms_allocated
                if f.id not in gh_r:
                    gh_r.append(f.id)
            gh_r = Rooms.objects.filter(guesthouse=t.guesthouse).filter(room_type=rtype)

            rooms = []
            for really in n_n:
                rooms.append(really.rooms_allocated)

            for rd in gh_r:
                if rd not in rooms:
                    xyz = rd
                    break

            newreservation = Reservation()
            newreservation.bookingID = (
                str(xyz.roomID) + str(user.username) + str(datetime.date.today())
            )
            newreservation.start_date = start_date
            newreservation.end_date = end_date
            # ...
            newreservation.number_rooms = number_rooms
            newreservation.number_children = number_children
            newreservation.number_adults = number_adults

            newreservation.user_booked = user
            newreservation.booktime = datetime.date.today()
            newreservation.guesthouse = t.guesthouse
            newreservation.status = True
            newreservation.room_type = rtype
            newreservation.rooms_allocated = xyz
            newreservation.save()
            newpayment = Payment()
            newpayment.paymentID = str(newreservation.bookingID) + str(
                xyz.price * (0.2)
            )
            newpayment.amount = xyz.price * 0.2
            newpayment.reservation = newreservation
            newpayment.user_booked = user
            newpayment.payment_time = datetime.date.today()
            newpayment.save()

            return render(
                request, "main/book_successful.html", {"reservation": newreservation}
            )
        else:
            messages.warning(request, "Requested Page Not Found ")
            return redirect("index")
    else:
        messages.warning(request, "You are not logged in. Please login")
        return redirect("login")


def cancel(request, id):
    user = request.user
    if user.username:

        reservation = Reservation.objects.get(id=id)
        reservation.status = False
        reservation.save()
        flag = 0

        for waiting_one in WaitingOn.objects.all():
            start_date = waiting_one.start_date
            end_date = waiting_one.end_date
            # ...
            number_rooms = waiting_one.number_rooms
            number_children = waiting_one.number_children
            number_adults = waiting_one.number_adults

            res_3 = waiting_one.resID

            n_n = (
                Reservation.objects.filter(
                    Q(start_date__range=(start_date, end_date))
                    | Q(end_date__range=(start_date, end_date))
                )
                .filter(status=True)
                .filter(waiting=False)
                .filter(room_type=res_3.room_type)
                .filter(guesthouse=res_3.guesthouse)
                .filter(
                    number_rooms=number_rooms,
                    number_children=number_children,
                    number_adults=number_adults,
                )
            )

            gh_r = Rooms.objects.filter(guesthouse=res_3.guesthouse).filter(
                room_type=res_3.room_type
            )

            rooms = []
            for really in n_n:
                f = really.rooms_allocated
                if f not in rooms:
                    rooms.append(f)

            for room_of in gh_r:
                if room_of not in rooms:
                    xyz = room_of
                    flag = 1

                    res_3.rooms_allocated = xyz
                    res_3.waiting = False
                    res_3.save()
                    waiting_one.delete()
                    break

            if flag == 1:
                break

        newrefund = Refund()
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
            request, "main/cancel_successful.html", {"reservation": reservation}
        )
    else:
        messages.warning(request, "you are not logged in or have no access")
        return redirect("login")


def my_bookings(request):
    user = request.user
    if user.username:
        n_n = (
            Reservation.objects.filter(user_booked=user)
            .order_by("-booktime")
            .filter(status=True)
        )
        bookings = []

        for t in n_n:
            g = t.guesthouse

            r_m = t.rooms_allocated
            bookings.append({"n_n": t, "gh_all": g, "gh_r": r_m})
        context = {"bookings": bookings, "reservation": n_n}
        return render(request, "main/my_bookings.html", context)
    else:
        messages.warning(
            request, "You are not authorized to acces the requested page. Please Login "
        )
        return redirect("login")


def waiting_show(request, t):
    user = request.user
    if user.username:
        if request.method == "POST":
            return redirect("index")
        else:
            e_s = PreReservation.objects.get(id=t)
            start_date = e_s.start_date
            end_date = e_s.end_date
            # ...
            number_rooms = e_s.number_rooms
            number_children = e_s.number_children
            number_adults = e_s.number_adults

            gh_all = GuestHouse.objects.all()
            context = []

            for g in gh_all:
                new_waiting = (
                    Reservation.objects.filter(
                        Q(start_date__range=(start_date, end_date))
                        | Q(end_date__range=(start_date, end_date))
                    )
                    .filter(status=True)
                    .filter(guesthouse=g)
                    .filter(
                        number_rooms=number_rooms,
                        number_children=number_children,
                        number_adults=number_adults,
                    )
                )

                rooms = []
                for b_a in new_waiting:
                    gh_r = b_a.room_type
                    flag = 0

                    for i in rooms:
                        if gh_r in i.values():
                            i["count"] = i["count"] + 1
                            flag = 1

                    if flag == 0:
                        rooms.append({"type": gh_r, "count": 1})

                context.append({"gh_all": g, "room2": rooms})
            return render(
                request, "main/waiting_show.html", {"rooms": context, "n_n": e_s}
            )
    else:
        messages.warning(request, "You are not logged in. Please login")
        redirect("login")


def waiting(request, g, t, rtype):
    user = request.user
    if user.username:
        if request.method == "POST":
            t = PreReservation.objects.get(id=t)
            t.guesthouse = GuestHouse.objects.get(id=g)
            t.save()

            newreservation = Reservation()
            newreservation.bookingID = str(t.guesthouse.code) + str(t.id)
            newreservation.start_date = t.start_date
            newreservation.end_date = t.end_date
            # ...
            newreservation.number_rooms = t.number_rooms
            newreservation.number_children = t.number_children
            newreservation.number_adults = t.number_adults

            newreservation.user_booked = user
            newreservation.room_type = rtype
            newreservation.booktime = datetime.date.today()
            newreservation.guesthouse = t.guesthouse
            newreservation.status = True
            newreservation.waiting = True
            newreservation.save()

            gh_r = Rooms.objects.filter(guesthouse=t.guesthouse).filter(room_type=rtype)

            newpayment = Payment()
            newpayment.paymentID = str(newreservation.bookingID) + str(
                gh_r[0].price * (0.2)
            )
            newpayment.amount = gh_r[0].price * (0.2)
            newpayment.reservation = newreservation
            newpayment.user_booked = user
            newpayment.payment_time = datetime.date.today()
            newpayment.save()
            newwaiting = WaitingOn()
            newwaiting.resID = newreservation
            newwaiting.date_booked = newreservation.booktime
            newwaiting.start_date = newreservation.start_date
            newwaiting.end_date = newreservation.end_date
            # ...
            newwaiting.number_rooms = newreservation.number_rooms
            newwaiting.number_children = newreservation.number_children
            newwaiting.number_adults = newreservation.number_adults
            newwaiting.save()

            return render(
                request,
                "main/waiting_successful.html",
                {
                    "reservation": newreservation,
                    "waiting": newwaiting,
                    "payment": newpayment,
                },
            )
        else:
            messages.warning(request, "Requested Page Not Found ")
            return redirect("index")
    else:
        messages.warning(request, "You are not logged in. Please login")
        return redirect("login")


def feedback(request):
    user = request.user
    if user.username:
        if request.method == "POST":
            form = FeedbackForm(request.POST)
            if form.is_valid():
                feed = form.cleaned_data.get("feed")
                newfeedback = Feedback()
                newfeedback.user_of = user
                newfeedback.time = date.today()
                newfeedback.feed = feed
                newfeedback.feedbackID = (
                    str(user.username) + str(date.today()) + str(user.email)
                )
                newfeedback.save()
                return render(request, "main/feedback_successful.html")
            else:
                messages.error(request, "Invalid form details")
        form = FeedbackForm()
        return render(request, "main/feedback.html", context={"form": form})
    else:
        messages.warning(request, "You are not logged in. Please login")
        redirect("login")


def cancelwaiting(request, id):
    user = request.user
    if user.username:

        reservation = Reservation.objects.get(id=id)
        reservation.status = False
        reservation.save()
        newrefund = Refund()
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
            request, "main/cancel_successful.html", {"reservation": reservation}
        )
    else:
        messages.warning(request, "you are not logged in or have no access")
        return redirect("login")


def gh_description(request, *args, **kwargs):
    user = request.user
    if user.username:
        ghdetails = get_object_or_404(GuestHouse, slug=kwargs.get("slug"))
    context = {"ghdetails": ghdetails}
    return render(request, "user/gh_description.html", context)


def room_description(request, *args, **kwargs):
    user = request.user
    if user.username:
        roomdetails = get_object_or_404(Rooms, slug=kwargs.get("slug"))
    context = {"roomdetails": roomdetails}
    return render(request, "user/room_description.html", context)
