
from django.views.static import serve
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from config.api import api


urlpatterns = (
    [
        path("admin/", admin.site.urls),
        path("", include("event.urls")),
        path("", include("main.urls")),
        path("", include("overview_correction.urls", namespace="overview_correction")),
        path("", include("restcomplex.urls")),
        path("", include("payments.urls")),
        path("", include("agent.urls")),
        path("", include("client.urls")),
        # ...
        path("likes/", include("likes.urls")),
        # ...
        path(
            "password-reset/",
            auth_views.PasswordResetView.as_view(
                template_name="event/password_reset.html"
            ),
            name="password_reset",
        ),
        path(
            "password-reset/done/",
            auth_views.PasswordResetDoneView.as_view(
                template_name="event/password_reset_done.html"
            ),
            name="password_reset_done",
        ),
        path(
            "password-reset-confirm/<uidb64>/<token>/",
            auth_views.PasswordResetConfirmView.as_view(
                template_name="event/password_reset_confirm.html"
            ),
            name="password_reset_confirm",
        ),
        path(
            "password-reset-complete/",
            auth_views.PasswordResetCompleteView.as_view(
                template_name="event/password_reset_complete.html"
            ),
            name="password_reset_complete",
        ),
        # ...
        path("", include("sendemail.urls")),
        path("search/", include("search.urls")),
        path("ckeditor/", include("ckeditor_uploader.urls")),
        path("ratings/", include("star_ratings.urls", namespace="ratings")),
        # ...
        path("api/", api.urls),


    ]
    + static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
)

urlpatterns += [
    path(
        "media/<path:path>",
        serve,
        {
            "document_root": settings.MEDIA_ROOT,
        },
    ),
    path("static/<path:path>", serve, {"document_root": settings.STATIC_ROOT}),
]
