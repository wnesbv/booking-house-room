
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from overview_correction.models import RentalServiceOffers, GHInfo, GHRooms


class AdminOffersForService(RentalServiceOffers):
    class Meta:
        proxy = True
        verbose_name = "1| admin offer service"
        verbose_name_plural = "1| admin offers services"

# ...
class GuestHouse(GHInfo):
    class Meta:
        proxy = True
        verbose_name = "2| admin guest house"
        verbose_name_plural = "2| admin guest house"

class Rooms(GHRooms):
    class Meta:
        proxy = True
        verbose_name = "3| admin room"
        verbose_name_plural = "3| admin rooms"
# ...

class Reservation(models.Model):
    bookingID = models.CharField(default=None, max_length=30)
    # ...
    start_date = models.DateTimeField(default=None, null=True)
    end_date = models.DateTimeField(default=None, null=True)

    # ...
    number_rooms = models.ForeignKey(
        GuestHouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="num_rooms_reserve",
        verbose_name="choosing the number of rooms",
    )
    number_children = models.ForeignKey(
        GuestHouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="num_children_reserve",
        verbose_name="choosing the number of children",
    )
    number_adults = models.ForeignKey(
        GuestHouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="num_adults_reserve",
        verbose_name="choosing the number of adults",
    )
    # ...
    user_booked = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=False, blank=False
    )
    rooms_allocated = models.ForeignKey(
        Rooms, on_delete=models.CASCADE, null=True, blank=True
    )
    guesthouse = models.ForeignKey(
        GuestHouse, on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.BooleanField(default=False)
    waiting = models.BooleanField(default=False)

    ROOM_TYPES = [
        ("01-Single", "01-Single"),
        ("02-Double", "02-Double"),
        ("03-Single-NON", "03-Single NON"),
        ("04-Double-NON", "04-Double-NON"),
    ]
    room_type = models.CharField(
        max_length=20, choices=ROOM_TYPES, null=True, blank=True
    )
    booktime = models.DateField(null=False)

    class Meta:
        verbose_name = "4| reservation"
        verbose_name_plural = "4| reservations"
        db_table = "OGHBS_Reservation"
        ordering = ["-booktime"]

    def __str__(self):
        return self.bookingID

class PreReservation(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # ...
    number_rooms = models.ForeignKey(
        GuestHouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="num_rooms_pre",
        verbose_name="choosing the number of rooms",
    )
    number_children = models.ForeignKey(
        GuestHouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="num_children_pre",
        verbose_name="choosing the number of children",
    )
    number_adults = models.ForeignKey(
        GuestHouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="num_adults_pre",
        verbose_name="choosing the number of adults",
    )
    # ...

    guesthouse = models.ForeignKey(
        GuestHouse, on_delete=models.CASCADE, null=True, blank=True
    )
    ROOM_TYPES = [
        ("01-Single", "01-Single"),
        ("02-Double", "02-Double"),
        ("03-Single-NON", "03-Single NON"),
        ("04-Double-NON", "04-Double-NON"),
    ]
    room_type = models.CharField(
        max_length=20, choices=ROOM_TYPES, null=True, blank=True
    )

    class Meta:
        verbose_name = "5| preliminary reservation"
        verbose_name_plural = "5| pre-reservations"

    def __str__(self):
        return (
            str(self.guesthouse)
            + " || "
            + str(self.start_date)
            + " - "
            + str(self.end_date)
        )


class Payment(models.Model):
    paymentID = models.CharField(default=None, max_length=30)
    amount = models.PositiveIntegerField(default=None, blank=False, null=False)
    reservation = models.ForeignKey(
        "Reservation", on_delete=models.CASCADE, related_name="payments"
    )
    user_booked = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False
    )
    payment_time = models.DateField(default=timezone.now, null=False)

    class Meta:
        verbose_name = "6| payment"
        verbose_name_plural = "6| payment"
        db_table = "OGHBS_Payments"
        ordering = ["-payment_time"]

    def __str__(self):
        return self.paymentID


class Refund(models.Model):
    refundID = models.CharField(default=None, max_length=30)
    payment = models.ForeignKey("Payment", on_delete=models.CASCADE)
    reservation = models.ForeignKey(
        "Reservation", on_delete=models.CASCADE, related_name="refunds"
    )
    amount = models.PositiveIntegerField(default=None, blank=False, null=False)
    user_booked = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False
    )
    refund_time = models.DateTimeField(null=False)

    class Meta:
        verbose_name = "7| refund"
        verbose_name_plural = "7| refund"
        db_table = "OGHBS_Refunds"
        ordering = ["-refund_time"]

    def __str__(self):
        return self.refundID


class Feedback(models.Model):
    feedbackID = models.CharField(default=None, max_length=100)
    user_of = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=False, blank=False
    )
    time = models.DateField(default=timezone.now, null=False)
    feed = models.TextField(default=None)

    class Meta:
        verbose_name = "8| feedback"
        verbose_name_plural = "8| feedback"
        db_table = "OGHBS_feedbacks"
        ordering = ["-time"]

    def __str__(self):
        return self.feedbackID


class WaitingOn(models.Model):
    resID = models.ForeignKey(
        "Reservation", on_delete=models.CASCADE, null=False, blank=False
    )
    # ...
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    # ...
    number_rooms = models.ForeignKey(
        GuestHouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="num_rooms_waiting",
        verbose_name="choosing the number of rooms",
    )
    number_children = models.ForeignKey(
        GuestHouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="num_children_waiting",
        verbose_name="choosing the number of children",
    )
    number_adults = models.ForeignKey(
        GuestHouse,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="num_adults_waiting",
        verbose_name="choosing the number of adults",
    )
    # ...

    date_booked = models.DateField(default=timezone.now, null=False)
