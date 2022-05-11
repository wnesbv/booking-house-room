
from django.urls import path
from django.views.generic.base import RedirectView
from django.contrib.auth import views as auth_views
from .import views


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="event/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="event/logout.html"),
        name="logout",
    ),
    path("register/", views.register, name="register"),
    path("activate/<uidb64>/<token>/", views.activate, name="activate"),
    path("profile/", views.profile, name="profile"),
    path("", RedirectView.as_view(url="home/")),
]
