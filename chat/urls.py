from django.urls import path
from . import views


app_name = "chat"

urlpatterns = [
    path("<int:recipient>/", views.ChatView.as_view(), name="chat"),
    path("send-message/", views.ChatView.as_view(), name="send-message"),
]
