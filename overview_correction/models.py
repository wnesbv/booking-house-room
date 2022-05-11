
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.text import slugify

from taggit.managers import TaggableManager
from cuser.middleware import CuserMiddleware
from ckeditor_uploader.fields import RichTextUploadingField

from restcomplex.models import RestComplex


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status="published")


class RentalServiceOffers(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    room_categories = models.CharField(
        choices=(
            ("No categories", "No categories"),
            ("Single", "Single"),
            ("Double", "Double"),
            ("Single-NON", "Single NON"),
            ("Double-NON", "Double-NON"),
        ),
        max_length=25,
        verbose_name="room categories",
    )
    functional_options = models.CharField(
        choices=(
            ("No special services", "No special services"),
            ("First special services", "First special services"),
            ("Second special services", "Second special services"),
            ("Third special services", "Third special services"),
            ("Final special services", "Final special services"),
        ),
        max_length=25,
        verbose_name="functionality",
    )
    slug = models.SlugField(max_length=50, unique=True)
    file_upload = models.FileField(
        default="default.json", upload_to="file_upload/%Y/%m/%d/"
    )
    tables_editing = RichTextUploadingField(
        default="Tables editing:01... offer service 01..."
    )
    inventory_offers = models.TextField(
        max_length=300,
        default="Inventory offers:01 offer service 01...",
        verbose_name="inventory offers",
    )

    class Meta:
        verbose_name = "1| Offers to supplement the rental services"
        verbose_name_plural = "1| Offers to supplement the rental services"
        db_table = "rental_service_offers"
        ordering = ["-functional_options"]

    def __str__(self):
        return str(self.room_categories) + " | " + str(self.functional_options)

    def save(self, *args, **kwargs):
        self.slug = slugify(
            str(self.room_categories) + " | " + str(self.functional_options)
        )
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "overview_correction:offers_for_detail", kwargs={"slug": self.slug}
        )

# ...
class GHInfo(models.Model):
    STATUS_CHOICES = (("draft", "Draft"), ("published", "Published"))
    name = models.CharField(
        default="GH-Name",
        max_length=25,
        null=False,
        unique=True,
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    functionality_gh = models.ForeignKey(
        RentalServiceOffers,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="functional options GH",
    )
    slug = models.SlugField(max_length=75, unique=True)
    # ...
    number_rooms = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="number of rooms",
    )
    number_children = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="number of children",
    )
    number_adults = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="number of adults",
    )
    code_g_f = models.CharField(
        choices=(
            ("01|one|gallery|filter", "01|one|gallery|filter"),
            ("02|two|gallery|filter", "02|two|gallery|filter"),
            ("03|three|gallery|filter", "03|three|gallery|filter"),
            ("04|four|gallery|filter", "04|four|gallery|filter"),
            ("05|five|gallery|filter", "05|five|gallery|filter"),
        ),
        null=True,
        blank=True,
        max_length=50,
        verbose_name="gallery filter",
    )
    figuratively = models.TextField(
        default="Figuratively:01.. GH-figuratively 01...", max_length=250
    )
    specifications = RichTextUploadingField(
        default="Specifications:01... GH-specifications 01...",
        null=True,
        blank=True,
    )
    # ...
    image = models.ImageField(default="g_h.jpg", upload_to="g_h_img")
    image_2 = models.ImageField(default="no_photo.jpg", upload_to="g_h_img")
    image_3 = models.ImageField(default="no_photo.jpg", upload_to="g_h_img")
    image_4 = models.ImageField(default="no_photo.jpg", upload_to="g_h_img")
    image_5 = models.ImageField(default="no_photo.jpg", upload_to="g_h_img")
    # ...
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    modified_at = models.DateTimeField("Дата изменения", auto_now=True)
    # ...
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    active = models.BooleanField(default=False)

    # ...
    objects = models.Manager()
    published = PublishedManager()
    tags = TaggableManager()

    class Meta:
        ordering = ("-modified_at",)
        verbose_name = "2| gh rooms info"
        verbose_name_plural = "2| gh rooms info"

    def __str__(self):
        return str(self.name) + " | " + str(self.functionality_gh)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name) + " | " + str(self.functionality_gh))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "overview_correction:gh_user_detail",
            kwargs={"slug": str(self.slug)},
        )

    @property
    def getLikeCount(self):
        return LikeDislike.objects.filter(rating_action=1, post__id=self.id).count()

    @property
    def getDislikeCount(self):
        return LikeDislike.objects.filter(rating_action=0, post__id=self.id).count()

    @property
    def getLikedUser(self):
        user = CuserMiddleware.get_user()
        count_liked = LikeDislike.objects.filter(
            rating_action=1, user=user, post__id=self.id
        ).count()
        if count_liked > 0:
            return True
        return False

    @property
    def getDisLikedUser(self):
        user = CuserMiddleware.get_user()
        count_disliked = LikeDislike.objects.filter(
            rating_action=0, user=user, post__id=self.id
        ).count()
        if count_disliked > 0:
            return True
        return False

# ...
class GHRooms(models.Model):
    ROOM_TYPES = [
        ("Single", "Single"),
        ("Double", "Double"),
        ("Single-NON", "Single NON"),
        ("Double-NON", "Double-NON"),
    ]
    ROOM_SERVICES = [
        ("no services", "no services"),
        ("first services", "first services"),
        ("second services", "second services"),
        ("third services", "third services"),
        ("final services", "final services"),
    ]
    # ...
    name = models.CharField(default=None, max_length=25, null=False, unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    # ...
    guesthouse = models.ForeignKey(
        GHInfo,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="choosing a guest house",
    )
    functionality_rm = models.ForeignKey(
        RentalServiceOffers,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="functional options rooms",
    )
    room_services = models.CharField(
        max_length=25, choices=ROOM_SERVICES, null=True, blank=True
    )
    room_type = models.CharField(
        max_length=25, choices=ROOM_TYPES, null=True, blank=True
    )
    room_specifications = models.TextField(
        default="room_specifications:01...", max_length=250, null=True, blank=True
    )
    slug = models.SlugField(
        default=None, max_length=75, unique=True, null=True, blank=True
    )
    price = models.PositiveIntegerField(default=None, null=True, blank=True)
    # ...
    img_logo = models.ImageField(default="l_r.jpg", upload_to="rooms_img")
    image = models.ImageField(default="room.jpg", upload_to="rooms_img")
    image_2 = models.ImageField(default="no_photo.jpg", upload_to="rooms_img")
    image_3 = models.ImageField(default="no_photo.jpg", upload_to="rooms_img")
    image_4 = models.ImageField(default="no_photo.jpg", upload_to="rooms_img")
    image_5 = models.ImageField(default="no_photo.jpg", upload_to="rooms_img")
    # ...
    active = models.BooleanField(default=False)
    # ...
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    modified_at = models.DateTimeField("Дата изменения", auto_now=True)

    class Meta:
        verbose_name = "3| gh room"
        verbose_name_plural = "3| gh rooms"
        db_table = "GH_Rooms"
        ordering = ["name"]

    def __str__(self):
        return (
            str(self.guesthouse) # 75
            + " | "
            + str(self.name) # 25
            + " | "
            + str(self.room_type) # 25
            + " | "
            + str(self.functionality_rm) # 50
            # 175
        )

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name) + " | " + str(self.room_services))
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            "overview_correction:room_user_detail",
            kwargs={"slug": str(self.slug)},
        )


# ...
class Comment(models.Model):
    post = models.ForeignKey(
        GHInfo, on_delete=models.CASCADE, related_name="gh_comments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("modified_at",)

    def __str__(self):
        return f"Comment by {self.user} on {self.post}"

    def get_absolute_url(self):
        return reverse(
            "overview_correction:gh_detail",
            kwargs={"slug": str(self.post.slug)},
        )

class Reply(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comment.post.pk} -- {self.comment.body} -- {self.reply}"

# ...
class LikeDislikeManager(models.Manager):
    def update_or_create_like(self, post_id, user_id):
        obj_user = User.objects.get(pk=user_id)
        obj, created = self.get_queryset().update_or_create(
            post_id=post_id,
            user=obj_user,
            defaults={"rating_action": 1},
        )
        return obj, created

    def update_or_create_dislike(self, post_id, user_id, *args, **kwargs):
        obj_user = User.objects.get(pk=user_id)
        obj, created = self.get_queryset().update_or_create(
            post_id=post_id,
            user=obj_user,
            defaults={"rating_action": 0},
        )
        return obj, created

    def delete_after_unlike(self, post_id, user_id, *args, **kwargs):
        obj_user = User.objects.get(pk=user_id)
        self.get_queryset().filter(post_id=post_id, user=obj_user).delete()

    def delete_after_undislike(self, post_id, user_id):
        obj_user = User.objects.get(pk=user_id)
        self.get_queryset().filter(post_id=post_id, user=obj_user).delete()

class LikeDislike(models.Model):
    post = models.ForeignKey(GHInfo, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating_action = models.CharField(max_length=30)

    def __str__(self):
        return self.post.name + " / " + self.user.username

    class Meta:
        unique_together = ("post", "user")

    objects = LikeDislikeManager()


# ... abstract
class Abstraction_Info(models.Model):
    name = models.CharField(
        default="Info About Us 01",
        max_length=100,
        null=True,
        blank=True,
    )
    # ...
    guest_house = models.ForeignKey(
        GHInfo,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="selecting a section guest house",
    )
    restcomplex_house = models.ForeignKey(
        RestComplex,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name="selecting a section restcomplex house",
    )
    # ...
    explanation = models.TextField(
        max_length=200,
        null=True,
        blank=True,
        default="explanation of the section:01...",
        verbose_name="explanation of the section",
    )
    other_photo = models.ImageField(default="g_h.jpg", upload_to="about_Us")

    # ...
    created_at = models.DateTimeField("Дата создания", auto_now_add=True)
    modified_at = models.DateTimeField("Дата изменения", auto_now=True)

    class Meta:
        abstract = True

class About_Us(Abstraction_Info):
    active_item = models.BooleanField(default=False)
    # ...
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey("content_type", "object_id")
    # ...

    class Meta:
        verbose_name = "about us"
        verbose_name_plural = "about us"
        ordering = ["modified_at"]

    def __str__(self):
        return self.name

class Info_About_Us(models.Model):
    name_gallery = models.CharField(
        default="information about-us 01",
        max_length=30,
        null=False,
        unique=True,
    )
    active_gallery = models.BooleanField(default=False)

    def __str__(self):
        return self.name_gallery

    class Meta:
        verbose_name = "information about us"
        verbose_name_plural = "information about us"
