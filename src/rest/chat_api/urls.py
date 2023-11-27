from django.urls import path

from . import views

urlpatterns = [
    path("chat-with/<int:user_id>/", views.PrivateMessageAPIView.as_view()),
]
