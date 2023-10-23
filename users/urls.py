from django.urls import path
from django.contrib.auth.views import LogoutView
from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from . import views

app_name = "users"


urlpatterns = [
    # register view
    path("register/", views.RegisterView.as_view(), name="register"),
    # login view
    path("login/", views.UserLoginView.as_view(), name="login"),
    # logout view
    path("logout/", login_required(LogoutView.as_view()), name="logout"),
    # profile view
    path("profile/", login_required(views.ProfileView.as_view()), name="profile"),
    path("options/", login_required(views.UserOptions.as_view()), name="options"),
    # profile another user
    path(
        "user_profile/<int:pk>/",
        login_required(views.UserProfileView.as_view()),
        name="another-user",
    ),
    # email verification
    path(
        "email-verification-sent/",
        lambda request: render(request, "users/register/email-verification-sent.html"),
        name="email-verification-sent",
    ),
    # followers
    path("follow-to/<int:user_id>/", login_required(views.follow), name="follow"),
]
