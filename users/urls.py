from django.urls import path
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from . import views

app_name = "users"


urlpatterns = [
    # register view
    path("register/", views.RegisterView.as_view(), name="register"),
    # login view
    path("login/", views.UserLoginView.as_view(), name="login"),
    # logout view
    path("logout/", LogoutView.as_view(), name="logout"),
    # profile view
    path("profile/", views.ProfileView.as_view(), name="profile"),
    # profile another user
    path("user_profile/<int:pk>/", views.UserProfile.as_view(), name="another-user"),
    # email verification
    path(
        "email-verification-sent/",
        lambda request: render(request, "users/register/email-verification-sent.html"),
        name="email-verification-sent",
    ),
]
