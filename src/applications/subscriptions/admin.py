from django.contrib import admin
from .models import BillingPlan, Subscription


admin.site.register(BillingPlan)

admin.site.register(Subscription)
