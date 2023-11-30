from .models import BillingPlan, Subscription
from rest_framework import serializers
from datetime import datetime, timedelta


class BillingPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingPlan
        fields = ["title", "price", "allowed_books", "send_message"]


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        abstact = True
        model = Subscription
        fields = ["user", "plan"]


class SelectSubscriptionSerializer(SubscriptionSerializer):
    user = serializers.IntegerField(read_only=True)
    period = serializers.IntegerField()

    class Meta:
        model = Subscription
        fields = SubscriptionSerializer.Meta.fields + ["period"]

    def create(self, validated_data):
        plan = BillingPlan.objects.get(title=validated_data.get("plan"))

        if not plan:
            raise ValueError("Plan with this ID doesn't exists")

        user = validated_data.get("user")
        subscription = Subscription.objects.filter(user=user, complete=True)

        if subscription.exists():
            raise ValueError("You cannot have two and more subcription")

        start = datetime.now()
        end = timedelta(days=validated_data.get("period") * 30)

        expired_date = start + end

        result = Subscription.objects.create(
            user=user, plan=plan, expires_date=expired_date
        )

        return result


class ReadSubscriptionSerializer(SelectSubscriptionSerializer):
    class Meta:
        SubscriptionSerializer.Meta.fields += ["complete"]
