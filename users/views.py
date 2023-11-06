from typing import Any

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView, UpdateView)

from book_relations.logic import get_user_rating

from .decorators import is_following, is_object_owner
from .forms import (EmailNewsLetterForm, LoginForm, MessageForm,
                    OptionalUserInformationForm, ProfileForm, RegisterForm)
from .models import User, UserEmailNewsLetter, UserFollowing, UserProfile
from .tasks import send_email_verification, send_message


class RegisterView(CreateView):
    """Registration form"""

    template_name = "users/register/register.html"
    model = User
    form_class = RegisterForm

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
            send_email_verification.delay(form.instance.email)
            return redirect("users:email-verification-sent")
        return HttpResponseRedirect(request.META["HTTP_REFERER"])


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


class UserUpdateView(UpdateView):
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

    def get_object(self, queryset=None):
        q = User.objects.all().select_related("profile")
        return super().get_object(queryset=q)

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        context = super().get_context_data(**kwargs)
        context["check_user"] = is_object_owner(self.request.user, obj)
        context["has_follow"] = is_following(self.request.user, obj)
        context["user_rating"] = get_user_rating(obj)
        return context


@login_required(redirect_field_name="users:login")
def follow(request, user_id):
    user = User.objects.get(id=user_id)
    if is_object_owner(request.user.id, user_id):
        return HttpResponseForbidden("Invalid")
    obj, create = UserFollowing.objects.get_or_create(
        user_id=user, followers_id=request.user
    )
    if not create:
        obj.delete()
    return HttpResponseRedirect(request.META["HTTP_REFERER"])


class UserOptionsView(TemplateView):
    template_name = "users/user-options.html"


class FollowersListView(ListView):
    template_name = "users/tables/followers-list.html"
    model = UserFollowing

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user).select_related("user_id")


class MyFollowingView(ListView):
    template_name = "users/tables/following-list.html"
    model = UserFollowing

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(followers_id=self.request.user).select_related("user_id")


class SendMailView(FormView):
    form_class = MessageForm

    def get(self, request, *args, **kwargs):
        if self.request.user.email == kwargs["email"]:
            raise PermissionDenied()
        form = MessageForm()
        return render(request, "users/send-mail.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = MessageForm(request.POST)
        if form.is_valid():
            to_email = kwargs.get("email")
            message = form.cleaned_data["message"]
            subject = form.cleaned_data["subject"]
            email = request.user.email

            send_message.delay(subject, message, email)

            user = User.objects.get(email=to_email)

            return redirect("users:another-user", pk=user.pk)
        return render(request, "users/send-mail.html", {"form": form})


class EmailNewsLetterView(UpdateView):
    template_name = "users/options/email-newsletter.html"
    model = UserEmailNewsLetter
    form_class = EmailNewsLetterForm
    success_url = reverse_lazy("users:newsletter")

    def get_object(self, queryset=None):
        obj, _ = UserEmailNewsLetter.objects.get_or_create(user=self.request.user)
        return obj
