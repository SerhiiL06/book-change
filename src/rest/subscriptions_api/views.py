from rest_framework.generics import ListAPIView, ListCreateAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.response import Response
from src.applications.subscriptions.models import BillingPlan, Subscription
from src.applications.subscriptions.serializers import (
    BillingPlanSerializer,
    SelectSubscriptionSerializer,
)

from django.urls import reverse
from src.applications.subscriptions.utils import StripeItems
from src.applications.subscriptions.logic import get_stripe_session

from django.conf import settings
import stripe


stripe.api_version = settings.STRIPE_VERSION
stripe.api_key = settings.STRIPE_SECRET_KEY


class BillingPlanAPIView(ListAPIView):
    queryset = BillingPlan.objects.all()
    serializer_class = BillingPlanSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "update"]

    def get_permissions(self):
        if self.request.method == "POST":
            return permissions.IsAdminUser

        return super().get_permissions()


class SubscriptionAPIView(ListCreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SelectSubscriptionSerializer

    def post(self, request):
        serializer = SelectSubscriptionSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user)

        item = request.data.get("period")

        items = StripeItems()
        session = stripe.checkout.Session.create(
            mode="subscription",
            success_url=request.build_absolute_uri(reverse("subscription_api:check")),
            cancel_url=request.build_absolute_uri(reverse("subscription_api:check")),
            line_items=[
                {
                    "price": items.ITEMS.get(item),
                    "quantity": int(serializer.validated_data.get("period")),
                }
            ],
        )

        self.request.session["stripe_key"] = session.id

        return Response({"status": session.url})


class CheckSubscriptionStatusAPIView(APIView):
    def get(self, request):
        stripe_key = self.request.session.get("stripe_key")

        subscription, session = get_stripe_session(stripe_id=stripe_key)

        if session.status == "complete":
            subscription.complete = True
            subscription.save()

            return Response("Well done", status=204)

        subscription.delete()

        return Response("Delete", status=204)
