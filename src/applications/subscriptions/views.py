from datetime import datetime, timedelta
from typing import Any

import stripe
from django.conf import settings
from django.contrib import messages
from django.shortcuts import (HttpResponseRedirect, get_object_or_404,
                              redirect, render)
from django.urls import reverse
from django.views.generic import FormView, ListView, View

from .forms import ChoicePeriodForm
from .logic import create_stripe_session, get_stripe_session
from .models import BillingPlan, Subscription
from .tasks import send_email_about_payment

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

        Subscription.objects.create(
            user=current_user, plan=plan, start_date=start, expires_date=end
        )

        item = plan.id

        session = create_stripe_session(request, item)

        self.request.session["stripe_key"] = session.id

        return redirect(session.url)


class SuccessCheckout(View):
    template_name = "subscription/success-checkout.html"

    def get(self, request, *args, **kwargs):
        stripe_id = self.request.session.get("stripe_key")

        subscription, session = get_stripe_session(stripe_id)

        if session.status == "complete":
            subscription.complete = True

            send_email_about_payment.delay(session)

            subscription.save()

            return render(request, "subscription/success-checkout.html")

        subscription.delete()

        subscription.save()
        return render(request, "subscription/cancel-checkout.html")
