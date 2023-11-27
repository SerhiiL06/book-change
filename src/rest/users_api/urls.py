from django.urls import path

from . import views

urlpatterns = [
    path("user-list/", views.UsersAPIView.as_view()),
    path("user-list/<int:pk>/", views.DetailUserAPIView.as_view()),
    path("my-followers/", views.MyFollowersAPIView.as_view()),
    path("my-subscriptions/", views.MyFollowingAPIView.as_view()),
    path("send-email/", views.SendEmailAPIView.as_view()),
    path("newsletter/", views.NewsLetterSettingsAPIView.as_view()),
]
