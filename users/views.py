from django.shortcuts import redirect, HttpResponseRedirect
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django_email_verification import send_email
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm
from .models import User


class RegisterView(CreateView):
    template_name = "users/register/register.html"
    model = User
    form_class = RegisterForm
    success_url = reverse_lazy("users:email-verifications-sent")

    def post(self, request, *args, **kwargs):
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

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(email=email, password=password)

        if user and user.is_active:
            login(request, user)
            return redirect("books:index")

        return HttpResponseRedirect(request.META["HTTP_REFERER"])
