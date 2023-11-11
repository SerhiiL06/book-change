from django.urls import path

from . import views

urlpatterns = [
    path("", views.BookRequestListAPIView.as_view()),
]
