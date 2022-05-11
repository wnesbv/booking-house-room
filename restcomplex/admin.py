
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import *


class RestOffersForAdmin(ImportExportModelAdmin):
    exclude = ("author",)
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    list_display = ("slug", "rest_complex", "functional_options")
    prepopulated_fields = {
        "slug": (
            "rest_complex",
            "functional_options",
        )
    }

class RestComplexAdmin(ImportExportModelAdmin):
    exclude = ("author",)
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)
    list_display = ("slug", "name", "functionality_rest", "function_code",)
    prepopulated_fields = {"slug": ("name", "functionality_rest")}


class KindOfRestAdmin(ImportExportModelAdmin):
    exclude = ("author",)
    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)

    prepopulated_fields = {
        "slug": ("name", "rest_services"),
        "name": ("recreation", "name", "rest_type", "functionality_kor"),
    }


admin.site.register(RestComplex, RestComplexAdmin)
admin.site.register(KindOfRest, KindOfRestAdmin)
admin.site.register(RestOffersFor, RestOffersForAdmin)
admin.site.register(ReservationRest)
admin.site.register(PreReservationRest)
admin.site.register(PaymentRest)
admin.site.register(RefundRest)
admin.site.register(FeedbackRest)
admin.site.register(WaitingOnRest)
