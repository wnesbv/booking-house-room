

from django.urls import path
from .views import search_gh, search_rest


urlpatterns = [
    path("search-gh/", search_gh, name="search_results_gh"),
    path("search-rest/", search_rest, name="search_results_rest"),
]
