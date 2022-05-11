
from import_export.admin import ImportExportModelAdmin
from django.contrib.admin import site
from .models import *


class AdminOffersForServiceAdmin(ImportExportModelAdmin):
    exclude = ("author", "slug",)
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

class GuestHouseAdmin(ImportExportModelAdmin):
    exclude = ("author", "slug",)
    list_display = (
        "name",
        "slug",
        "author",
        "status",
        "active",
    )
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

class RoomsAdmin(ImportExportModelAdmin):
    exclude = ("author", "slug",)
    list_display = (
        "name",
        "slug",
        "author",
        "price",
        "active",
    )

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)



site.register(GuestHouse, GuestHouseAdmin)
site.register(Rooms, RoomsAdmin)
site.register(AdminOffersForService, AdminOffersForServiceAdmin)
site.register(Reservation)
site.register(PreReservation)
site.register(Payment)
site.register(Refund)
site.register(Feedback)
site.register(WaitingOn)
