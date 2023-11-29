from django.urls import path

from . import views

app_name = "subscription"


urlpatterns = [
    path("list/", views.ChoicePlanView.as_view(), name="plan-list"),
    path("success/", views.SuccessCheckout.as_view(), name="success"),
    path("<str:plan>/", views.ChoicePeriodView.as_view(), name="period"),
]
