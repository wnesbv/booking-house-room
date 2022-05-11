

from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import ModelAdmin, site
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import (
    About_Us,
    Info_About_Us,
    Comment,
    Reply,
    LikeDislike,
)


# ...
class About_UsInline(GenericTabularInline):
    model = About_Us
    extra = 0
    fields = (
        "name",
        "guest_house",
        "restcomplex_house",
        "explanation",
        "other_photo",
        "active_item",
    )

class Info_About_UsAdmin(ImportExportModelAdmin):
    list_display = (
        "name_gallery",
        "active_gallery",
    )
    inlines = [
        About_UsInline,
    ]


# ...
class CommentAdmin(ModelAdmin):
    list_display = ("user", "email", "post", "active")

class ReplyAdmin(ModelAdmin):
    list_display = (
        "user",
        "created_at",
    )

class LikeDislikeAdmin(ModelAdmin):
    list_display = (
        "user",
        "post",
        "rating_action",
    )


site.register(Info_About_Us, Info_About_UsAdmin)
# ...
site.register(Comment, CommentAdmin)
site.register(Reply, ReplyAdmin)
site.register(LikeDislike, LikeDislikeAdmin)
