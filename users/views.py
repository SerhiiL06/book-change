from typing import Any
from django.shortcuts import redirect, HttpResponseRedirect
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django_email_verification import send_email
from .models import UserFollowing
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
        form = ProfileForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()

        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class UserProfile(DetailView):
    template_name = "users/user-profile.html"
    model = User
    context_object_name = "profile"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        users = self.request.user == self.get_object()
        context["check_user"] = users
        context["has_follow"] = UserFollowing.objects.filter(
            followers_id=self.request.user, user_id=self.get_object()
        ).exists()
        print(context["has_follow"])
        return context


def follow(request, user_id):
    follower = User.objects.get(id=request.user.id)
    follow_to = User.objects.get(id=user_id)
    obj = UserFollowing.objects.filter(user_id=follow_to, followers_id=follower)
    if obj.first():
        obj.delete()
    else:
        UserFollowing.objects.create(user_id=follow_to, followers_id=follower)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class UserOptions(TemplateView):
    template_name = "users/user-options.html"
