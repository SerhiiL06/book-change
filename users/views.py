from typing import Any
from django.shortcuts import redirect, HttpResponseRedirect, render
from django.views.generic import CreateView, UpdateView, DetailView, TemplateView
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, authenticate
from django_email_verification import send_email
from .models import UserFollowing, UserProfile
from django.urls import reverse_lazy

from .forms import RegisterForm, LoginForm, ProfileForm, OptionalUserInformationForm
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
    form_class = OptionalUserInformationForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user

    def get(self, request, *args, **kwargs):
        profile, create = UserProfile.objects.get_or_create(user=request.user)
        form = ProfileForm(instance=request.user)
        profile_form = OptionalUserInformationForm(instance=profile)
        context = {"form": form, "profile_form": profile_form}
        return render(request, "users/profile.html", context)

    def post(self, request, *args, **kwargs):
        profile, create = UserProfile.objects.get_or_create(user=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = OptionalUserInformationForm(request.POST, instance=profile)

        if profile_form.is_valid() and form.is_valid():
            profile_form.save()
            form.save()

        return HttpResponseRedirect(request.META["HTTP_REFERER"])


class GeneralProfileView(DetailView):
    template_name = "users/user-profile.html"
    model = User
    context_object_name = "object"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        users = self.request.user == self.get_object()
        context["check_user"] = users
        context["has_follow"] = UserFollowing.objects.filter(
            followers_id=self.request.user, user_id=self.get_object()
        ).exists()
        return context


@login_required(redirect_field_name="users:login")
def follow(request, user_id):
    follower = User.objects.get(id=request.user.id)
    follow_to = User.objects.get(id=user_id)
    if follow == follow_to:
        return HttpResponseForbidden("Invalid")
    obj = UserFollowing.objects.filter(user_id=follow_to, followers_id=follower)
    if obj.first():
        obj.delete()
    else:
        UserFollowing.objects.create(user_id=follow_to, followers_id=follower)
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class UserOptions(TemplateView):
    template_name = "users/user-options.html"
