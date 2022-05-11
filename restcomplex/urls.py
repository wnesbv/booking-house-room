

from django.urls import path
from django.views.generic import ListView, DetailView
from .import views
from .models import RestOffersFor


urlpatterns = [
    path("home-rest/", views.HomeRestListView.as_view(), name="home_rest"),
    path("rest-book/", views.index, name="index_rest"),
    path("fitness/", views.fitness, name="fitness"),
    path("my-bookings/", views.my_bookings, name="my_bookings_rest"),
    path("query/", views.query, name="query_rest"),
    path("book-rest/<int:t>", views.book, name="book_rest"),
    path(
        "book-rest/<int:g>/<int:t>/<slug:rtype>/<int:count>/",
        views.book_rest_verify,
        name="book_rest_verify_rest",
    ),
    path("cancel-rest/<int:id>/", views.cancel, name="cancel_rest"),
    path("cancel_waiting-rest/<int:id>/", views.cancelwaiting, name="cancelwaiting_rest"),
    path("waiting-rest/<int:t>/", views.waiting_show, name="waiting_show_rest"),
    path("waiting-rest/<int:g>/<int:t>/<slug:rtype>/", views.waiting, name="waiting_rest"),
    path("feedback-rest/", views.feedback, name="feedback_rest"),
    path("restdetails/<slug:slug>", views.roomdetails, name="restdetails"),
    path("rc-details/<slug:slug>", views.rc_details, name="r_c_details"),
    # ...
    path(
        "offers-rest",
        ListView.as_view(model=RestOffersFor, paginate_by=2),
        name="offers_for_rest",
    ),
    path(
        "offers-rest-detail/<slug:slug>",
        DetailView.as_view(slug_field="slug", model=RestOffersFor),
        name="offers_rest_detail",
    ),

]
