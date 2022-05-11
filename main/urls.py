

from django.urls import path
from main import views

urlpatterns = [

    path("index-book/", views.index, name="index"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("query/", views.query, name="query"),
    path("book/<int:t>", views.book, name="book"),
    path(
        "book/<int:g>/<int:t>/<slug:rtype>/<int:count>/",
        views.book_room_verify,
        name="book_room_verify",
    ),
    path("cancel/<int:id>/", views.cancel, name="cancel"),
    path("cancel_waiting/<int:id>/", views.cancelwaiting, name="cancelwaiting"),
    path("waiting/<int:t>/", views.waiting_show, name="waiting_show"),
    path("waiting/<int:g>/<int:t>/<slug:rtype>/", views.waiting, name="waiting"),
    path("feedback/", views.feedback, name="feedback"),
    path("gh-main-detail/<slug:slug>", views.gh_description, name="gh_main_detail"),
    path("room-description/<slug:slug>", views.room_description, name="room_description"),


]
