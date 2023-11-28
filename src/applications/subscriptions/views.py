from typing import Any
from django.shortcuts import get_object_or_404, HttpResponseRedirect, redirect
from django.views.generic import ListView, FormView, TemplateView
from .models import BillingPlan, Subscription
from django.urls import reverse
from django.contrib import messages
from .forms import ChoicePeriodForm
from datetime import datetime, timedelta
from django.conf import settings
import stripe


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
        plan = get_object_or_404(BillingPlan, title=self.kwargs.get("plan"))

        subscription_result = Subscription.objects.filter(user=current_user, plan=plan)

        if subscription_result.first():
            messages.warning(request, "Your are have current plan")
            return HttpResponseRedirect(request.META["HTTP_REFERER"])

        start = datetime.now()

        period = int(request.POST["plan_period"]) * 30

        end = start + timedelta(days=period)

        new = Subscription(
            user=current_user, plan=plan, start_date=start, expires_date=end
        )

        session = stripe.checkout.Session.create(
            success_url=request.build_absolute_uri(reverse("subscription:success")),
            cancel_url=request.build_absolute_uri(reverse("subscription:cancel")),
            mode="subscription",
            line_items=[
                {
                    "price": "price_1OHU0wARKZme3upq8axaymaU",
                    "quantity": int(request.POST["plan_period"]),
                },
            ],
        )

        new.save()

        return redirect(session.url)


class SuccessCheckout(TemplateView):
    template_name = "subscription/success-checkout.html"
