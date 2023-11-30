from .models import Subscription
from django.contrib.auth import get_user_model
from django.urls import reverse
from .utils import StripeItems


import stripe


def create_stripe_session(request, item):
    items = StripeItems()
    session = stripe.checkout.Session.create(
        success_url=request.build_absolute_uri(reverse("subscription:success")),
        cancel_url=request.build_absolute_uri(reverse("subscription:success")),
        mode="subscription",
        line_items=[
            {
                "price": items.ITEMS.get(item),
                "quantity": int(request.POST["plan_period"]),
            },
        ],
    )
    return session


def get_stripe_session(stripe_id):
    current_session = stripe.checkout.Session.retrieve(id=stripe_id)

    user_email = current_session.customer_details.email

    user = get_user_model().objects.get(email=user_email)

    subscription = Subscription.objects.filter(user=user).last()

    return [subscription, current_session]
