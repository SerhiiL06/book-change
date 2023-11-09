from django.urls import path
from . import views

urlpatterns = [
    path("user-list/", views.UsersAPIView.as_view()),
    path("user-list/<int:user_id>/", views.DetailUserAPIView.as_view()),
    path("send-email/", views.SendEmailAPIView.as_view()),
]
