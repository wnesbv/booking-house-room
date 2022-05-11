from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor_uploader.fields import RichTextUploadingField


class RestOffersFor(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rest_complex = models.CharField(
        choices=(
            ("01|sauna", "01|sauna"),
            ("02|billiards", "02|billiards"),
            ("03|massage", "03|massage"),
            ("04|acupuncture", "04|acupuncture"),
        ),
        max_length=25,
        verbose_name="rest kinds",
    )
    functional_options = models.CharField(
        choices=(
            ("no additionally", "no additionally"),
            ("01|one additionally", "01|one additionally"),
            ("02|two additionally", "02|two additionally"),
            ("03|three additionally", "03|three additionally"),
            ("04|four additionally", "04|four additionally"),
            ("05|five additionally", "05|five additionally"),
        ),
        max_length=25,
        verbose_name="functionality",
    )
    slug = models.SlugField(max_length=50, unique=True)
    file_upload = models.FileField(
        default="default.json", upload_to="file_upload/%Y/%m/%d/"
    )
    tables_editing = RichTextUploadingField(
        default="Tables editing:01... Service to rest 01..."
    )
    inventory_offers = models.TextField(
        max_length=300,
        default="Inventory offers:01... Service to rest 01...",
        verbose_name="inventory offers",
    )

    class Meta:
        verbose_name = "1| service to rest"
        verbose_name_plural = "1| service to rest"
        db_table = "service_to_rest"
        ordering = ["-functional_options"]

    def __str__(self):
        return str(self.rest_complex) + " | " + str(self.functional_options)

    def get_absolute_url(self):
        return reverse("offers_rest_detail", kwargs={"slug": self.slug})


class RestComplex(models.Model):
    name = models.CharField(
        default="RestComplex-Name", max_length=25, null=False, unique=True
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=3, null=True, unique=True)
    functionality_rest = models.ForeignKey(
        RestOffersFor,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="functional options RestComplex",
    )
    function_code = models.CharField(
        choices=(
            ("01|one|rest|filter", "01one|rest|filter"),
            ("02|two|rest|filter", "02|two|rest|filter"),
            ("03|three|rest|filter", "03|three|rest|filter"),
            ("04|four|rest|filter", "04|four|rest|filter"),
            ("05|five|rest|filter", "05|five|rest|filter"),
        ),
        max_length=25,
        verbose_name="rest filter",
    )
    slug = models.SlugField(max_length=75, unique=True)
    figuratively_rest = models.TextField(
        default="Figuratively rest:01.. RC-figuratively 01...", max_length=300
    )
    specifications_rest = RichTextUploadingField(
        default="Specifications rest:01... RC-specifications 01..."
    )
    image = models.ImageField(default="fitness.svg", upload_to="fitness", blank=True)
    hede = models.CharField(default="T-Header", max_length=30, blank=True)
    expe = models.TextField(default="T-Explanations", max_length=50, blank=True)
    disc = models.TextField(default="P-Explained", max_length=100, blank=True)

    image_2 = models.ImageField(default="no_photo.jpg", upload_to="fitness", blank=True)
    hede_2 = models.CharField(default="T-Header-02", max_length=30, blank=True)
    expe_2 = models.TextField(default="T-Explanations-02", max_length=50, blank=True)
    disc_2 = models.TextField(default="P-Explained-02", max_length=100, blank=True)

    image_3 = models.ImageField(default="no_photo.jpg", upload_to="fitness", blank=True)
    hede_3 = models.CharField(default="T-Header-03", max_length=30, blank=True)
    expe_3 = models.TextField(default="T-Explanations-03", max_length=50, blank=True)
    disc_3 = models.TextField(default="P-Explained-03", max_length=100, blank=True)

    image_4 = models.ImageField(default="no_photo.jpg", upload_to="fitness", blank=True)
    hede_4 = models.CharField(default="T-Header-04", max_length=30, blank=True)
    expe_4 = models.TextField(default="T-Explanations-04", max_length=50, blank=True)
    disc_4 = models.TextField(default="P-Explained-04", max_length=100, blank=True)

    image_5 = models.ImageField(default="no_photo.jpg", upload_to="fitness", blank=True)
    hede_5 = models.CharField(default="T-Header-05", max_length=30, blank=True)
    expe_5 = models.TextField(default="T-Explanations-05", max_length=50, blank=True)
    disc_5 = models.TextField(default="P-Explained-05", max_length=100, blank=True)

    image_6 = models.ImageField(default="no_photo.jpg", upload_to="fitness", blank=True)
    hede_6 = models.CharField(default="T-Header-06", max_length=30, blank=True)
    expe_6 = models.TextField(default="T-Explanations-06", max_length=50, blank=True)
    disc_6 = models.TextField(default="P-Explained-06", max_length=100, blank=True)

    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "2| rest complex"
        verbose_name_plural = "2| rest complex"

    def __str__(self):
        return self.name


# ...
class KindOfRest(models.Model):
    REST_TYPES = [
        ("01-sauna", "01-sauna"),
        ("02-billiards", "02-billiards"),
        ("03-massage", "03-massage"),
        ("04-acupuncture", "04-acupuncture"),
    ]
    REST_SERVICES = [
        ("01-one services", "01-one services"),
        ("02-two services", "02-two services"),
        ("03-three services", "03-three services"),
        ("04-four services", "04-four services"),
        ("05-five services", "05-five services"),
    ]
    name = models.CharField(default="KR-Name", max_length=25, null=False, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    recreation = models.ForeignKey(
        RestComplex,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    functionality_kor = models.ForeignKey(
        RestOffersFor,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="functional options rest",
    )

    rest_services = models.CharField(
        max_length=25, choices=REST_SERVICES, null=True, blank=True
    )
    rest_type = models.CharField(
        max_length=25, choices=REST_TYPES, null=True, blank=True
    )
    slug = models.SlugField(max_length=75, unique=True)
    price = models.PositiveIntegerField(default=None, blank=False, null=False)
    img_logo = models.ImageField(default="l_r.jpg", upload_to="services_img")

    image = models.ImageField(default="services.svg", upload_to="services_img")
    hede = models.CharField(default="T-Header", max_length=30, blank=True)
    expe = models.TextField(default="T-Explanations", max_length=50, blank=True)
    disc = models.TextField(default="P-Explained", max_length=100, blank=True)

    image_2 = models.ImageField(default="no_photo.jpg", upload_to="services_img")
    hede_2 = models.CharField(default="T-Header-02", max_length=30, blank=True)
    expe_2 = models.TextField(default="T-Explanations-02", max_length=50, blank=True)
    disc_2 = models.TextField(default="P-Explained-02", max_length=100, blank=True)

    image_3 = models.ImageField(default="no_photo.jpg", upload_to="services_img")
    hede_3 = models.CharField(default="T-Header-03", max_length=30, blank=True)
    expe_3 = models.TextField(default="T-Explanations-03", max_length=50, blank=True)
    disc_3 = models.TextField(default="P-Explained-03", max_length=100, blank=True)

    image_4 = models.ImageField(default="no_photo.jpg", upload_to="services_img")
    hede_4 = models.CharField(default="T-Header-04", max_length=30, blank=True)
    expe_4 = models.TextField(default="T-Explanations-04", max_length=50, blank=True)
    disc_4 = models.TextField(default="P-Explained-04", max_length=100, blank=True)

    image_5 = models.ImageField(default="no_photo.jpg", upload_to="services_img")
    hede_5 = models.CharField(default="T-Header-05", max_length=30, blank=True)
    expe_5 = models.TextField(default="T-Explanations-05", max_length=50, blank=True)
    disc_5 = models.TextField(default="P-Explained-05", max_length=100, blank=True)

    image_6 = models.ImageField(default="no_photo.jpg", upload_to="fitness", blank=True)
    hede_6 = models.CharField(default="T-Header-06", max_length=30, blank=True)
    expe_6 = models.TextField(default="T-Explanations-06", max_length=50, blank=True)
    disc_6 = models.TextField(default="P-Explained-06", max_length=100, blank=True)

    class Meta:
        verbose_name = "3| kind rest"
        verbose_name_plural = "3| kind rest"
        db_table = "kind_rest"
        ordering = ["name"]

    def __str__(self):
        return self.name


class ReservationRest(models.Model):
    bookingID = models.CharField(default=None, max_length=30)
    start_date = models.DateTimeField(default=None, null=True)
    end_date = models.DateTimeField(default=None, null=True)
    user_booked = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=False, blank=False
    )
    rooms_allocated = models.ForeignKey(
        KindOfRest, on_delete=models.CASCADE, null=True, blank=True
    )
    recreation = models.ForeignKey(
        RestComplex, on_delete=models.CASCADE, null=True, blank=True
    )
    status = models.BooleanField(default=False)
    waiting = models.BooleanField(default=False)

    REST_TYPES = [
        ("01-sauna", "01-sauna"),
        ("02-billiards", "02-billiards"),
        ("03-massage", "03-massage"),
        ("04-acupuncture", "04-acupuncture"),
    ]
    rest_type = models.CharField(
        max_length=25, choices=REST_TYPES, null=True, blank=True
    )
    booktime = models.DateField(null=False)

    class Meta:
        verbose_name = "4| reservation rest"
        verbose_name_plural = "4| reservations rest"
        db_table = "reservations_rest"
        ordering = ["-booktime"]

    def __str__(self):
        return self.bookingID


class PreReservationRest(models.Model):
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    # no_rooms = models.IntegerField(null=True, blank=True)
    recreation = models.ForeignKey(
        RestComplex, on_delete=models.CASCADE, null=True, blank=True
    )
    REST_TYPES = [
        ("01-sauna", "01-sauna"),
        ("02-billiards", "02-billiards"),
        ("03-massage", "03-massage"),
        ("04-acupuncture", "04-acupuncture"),
    ]
    rest_type = models.CharField(
        max_length=20, choices=REST_TYPES, null=True, blank=True
    )

    class Meta:
        verbose_name = "5| preliminary reservation rest"
        verbose_name_plural = "5| pre reservations rest"

    def __str__(self):
        return (
            str(self.recreation)
            + " || "
            + str(self.start_date)
            + " - "
            + str(self.end_date)
        )


class PaymentRest(models.Model):
    paymentID = models.CharField(default=None, max_length=30)
    amount = models.PositiveIntegerField(default=None, blank=False, null=False)
    reservation = models.ForeignKey(
        "ReservationRest", on_delete=models.CASCADE, related_name="payments"
    )
    user_booked = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False
    )
    payment_time = models.DateField(default=timezone.now, null=False)

    class Meta:
        verbose_name = "6| payment rest"
        verbose_name_plural = "6| payment rest"
        db_table = "payment_rest"
        ordering = ["-payment_time"]

    def __str__(self):
        return self.paymentID


class RefundRest(models.Model):
    refundID = models.CharField(default=None, max_length=30)
    payment = models.ForeignKey("PaymentRest", on_delete=models.CASCADE)
    reservation = models.ForeignKey(
        "ReservationRest", on_delete=models.CASCADE, related_name="refunds"
    )
    amount = models.PositiveIntegerField(default=None, blank=False, null=False)
    user_booked = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, blank=False
    )
    refund_time = models.DateTimeField(null=False)

    class Meta:
        verbose_name = "7| refund rest"
        verbose_name_plural = "7| refund rest"
        db_table = "refund_rest"
        ordering = ["-refund_time"]

    def __str__(self):
        return self.refundID


class FeedbackRest(models.Model):
    feedbackID = models.CharField(default=None, max_length=100)
    user_of = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=False, blank=False
    )
    time = models.DateField(default=timezone.now, null=False)
    feed = models.TextField(default=None)

    class Meta:
        verbose_name = "8| feedback rest"
        verbose_name_plural = "8| feedback rest"
        db_table = "feedback_rest"
        ordering = ["-time"]

    def __str__(self):
        return self.feedbackID


class WaitingOnRest(models.Model):
    resID = models.ForeignKey(
        "ReservationRest", on_delete=models.CASCADE, null=False, blank=False
    )
    date_booked = models.DateField(default=timezone.now, null=False)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
