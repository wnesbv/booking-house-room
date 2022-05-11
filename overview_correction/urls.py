

from django.urls import path
from django.views.generic import ListView, DetailView
from overview_correction import views
from overview_correction.models import RentalServiceOffers, About_Us, GHRooms

app_name = "overview_correction"

urlpatterns = [
    path("home/", views.SliderGHListView.as_view(), name="home"),
        # path("about/", views.about, name="about"),
    path("about/", ListView.as_view(model=About_Us, paginate_by=2), name="about"),

    # ...
    path(
        "offers-for",
        ListView.as_view(model=RentalServiceOffers, paginate_by=2),
        name="offers_for",
    ),
    path(
        "offers-for/<slug:slug>",
        DetailView.as_view(slug_field="slug", model=RentalServiceOffers),
        name="offers_for_detail",
    ),
    # ...
    path("gh-list/", views.GHListView.as_view(), name="gh_list"),
    path(
        "gh-detail/<slug:slug>/",
        views.GHDetailView.as_view(),
        name="gh_detail",
    ),
    # ...
    path(
        "rooms-list",
        ListView.as_view(model=GHRooms, paginate_by=2),
        name="rooms_list",
    ),
    path(
        "room-detail/<slug:slug>",
        DetailView.as_view(model=GHRooms),
        name="room_detail",
    ),

    # ...
    path("gh-user-list/", views.UserGHListView.as_view(), name="gh_user_list"),
    path(
        "gh-user-detail/<slug:slug>/",
        views.UserGHDetailView.as_view(),
        name="gh_user_detail",
    ),
    # ...
    path("rooms-user-list/", views.UserRoomsListView.as_view(), name="rooms_user_list"),
    path(
        "room-user-detail/<slug:slug>/",
        views.UserRoomsDetailView.as_view(),
        name="room_user_detail",
    ),

    # ...
    path("gh-create", views.UserGHCreateView.as_view(), name="create_gh"),
    path(
        "<slug:slug>/update/",
        views.UserGHUpdate.as_view(),
        name="gh_update",
    ),
    path(
        "<slug:slug>/delete/",
        views.UserGHDelete.as_view(),
        name="gh_delete",
    ),
    # ...
    path("room-create", views.UserRoomCreateView.as_view(), name="create_room"),
    path(
        "<slug:slug>/room-update/",
        views.UserRoomUpdate.as_view(),
        name="room_update",
    ),
    path(
        "<slug:slug>/room-delete/",
        views.UserRoomDelete.as_view(),
        name="room_delete",
    ),

    # ...
    path("tag/<slug:tag_slug>/", views.GHListView.as_view(), name="gh_list_by_tag"),

    # ...
    path("reply/<int:pk>/", views.ReplyView.as_view(), name="reply"),
    # ...
    path("<int:post_id>/gh-share/", views.PostShareView.as_view(), name="gh_share"),
     # ....
    path("reply/<int:pk>/remove/", views.rply_remove, name="reply_remove"),
    path("comment/<int:pk>/remove/", views.comment_remove, name="comment_remove"),

]
