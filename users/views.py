from typing import Any
from django.db import models
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django_email_verification import send_email
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, ProfileForm
from .models import User


class RegisterView(CreateView):
    template_name = "users/register/register.html"
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy("users:email-verifications-sent")

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            send_email(user)
            return redirect("users:email-verification-sent")
        else:
            return HttpResponseRedirect("users:register")


class UserLoginView(LoginView):
    template_name = "users/login/login.html"
    form_class = LoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("books:index")

    def post(self, request):
        form = LoginForm(request.POST)

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)

        if user and user.is_active:
            login(request, user)
            return redirect("books:index")

        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class ProfileView(UpdateView):
    template_name = "users/profile.html"
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST, instance=request.user)
        print(request.POST)

        if form.is_valid():
            user = form.save()
            user.image = request.POST.get("image")
            user.save()

        return HttpResponseRedirect(request.META["HTTP_REFERER"])
