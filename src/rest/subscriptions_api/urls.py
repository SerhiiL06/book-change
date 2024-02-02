from django.urls import path

from . import views

app_name = "subscription_api"

urlpatterns = [
    path("list/", views.BillingPlanAPIView.as_view()),
    path("period/", views.SubscriptionAPIView.as_view()),
    path("success/", views.CheckSubscriptionStatusAPIView.as_view(), name="check"),
]
