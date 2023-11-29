from datetime import datetime, timedelta
from typing import Any

import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.generic import FormView, ListView, TemplateView, View

from src.applications.users.models import User

from .forms import ChoicePeriodForm
from .models import BillingPlan, Subscription
from .utils import StripeItems

stripe.api_version = settings.STRIPE_VERSION
stripe.api_key = settings.STRIPE_SECRET_KEY


class ChoicePlanView(ListView):
    template_name = "subscription/choice-plan.html"
    queryset = BillingPlan.objects.exclude(title="Free Plan")


class ChoicePeriodView(FormView):
    template_name = "subscription/choice-period.html"
    form_class = ChoicePeriodForm

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["select_plan"] = self.kwargs.get("plan")

        return context

    def post(self, request, *args, **kwargs):
        current_user = request.user
        title_plan = self.kwargs.get("plan")
        plan = get_object_or_404(BillingPlan, title=title_plan)

        subscription_result = Subscription.objects.filter(
            user=current_user, complete=True
        )

        if subscription_result.first():
            messages.warning(request, "Your are have current plan")
            return HttpResponseRedirect("books:index")

        start = datetime.now()

        period = int(request.POST["plan_period"]) * 30

        end = start + timedelta(days=period)

        new = Subscription(
            user=current_user, plan=plan, start_date=start, expires_date=end
        )

        items = StripeItems()

        item = title_plan.split()[0]

        session = stripe.checkout.Session.create(
            success_url=request.build_absolute_uri(reverse("subscription:success")),
            cancel_url=request.build_absolute_uri(reverse("subscription:cancel")),
            mode="subscription",
            line_items=[
                {
                    "price": items.ITEMS.get(item),
                    "quantity": int(request.POST["plan_period"]),
                },
            ],
        )

        self.request.session["stripe_key"] = session.id

        new.save()

        return redirect(session.url)


class SuccessCheckout(View):
    template_name = "subscription/success-checkout.html"

    def get(self, request, *args, **kwargs):
        stripe_id = self.request.session.get("stripe_key")
        current_session = stripe.checkout.Session.retrieve(id=stripe_id)

        user_email = current_session.customer_details.email

        user = User.objects.get(email=user_email)

        subscription = Subscription.objects.filter(user=user).last()

        if current_session.status == "complete":
            subscription.complete = True

            subscription.save()

            return render(request, "subscription/success-checkout.html")

        subscription.delete()

        subscription.save()
        return render(request, "subscription/cancel-checkout.html")
