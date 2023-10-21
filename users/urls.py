from django.urls import path
from django.shortcuts import render
from django_email_verification import urls as email_urls
from . import views

app_name = "users"


urlpatterns = [
    # register view
    path("register/", views.RegisterView.as_view(), name="register"),
    # login view
    path("login/", views.UserLoginView.as_view(), name="login"),
    # email verification
    path(
        "email-verification-sent/",
        lambda request: render(request, "users/register/email-verification-sent.html"),
        name="email-verification-sent",
    ),
]
