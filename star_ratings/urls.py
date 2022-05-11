

from django.urls import path
from .views import Rate
from .import app_settings

app_name = "star_ratings"

urlpatterns = [
    path(
        "(<content_type_id>/<object_id>"
        + app_settings.STAR_RATINGS_OBJECT_ID_PATTERN
        + "/",
        Rate.as_view(),
        name="rate",
    ),
]
