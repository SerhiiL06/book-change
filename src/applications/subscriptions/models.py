from django.contrib.auth import get_user_model
from django.db import models


class BillingPlan(models.Model):
    title = models.CharField(max_length=50, unique=True, db_index=True)

    price = models.DecimalField(max_digits=3, decimal_places=0)

    allowed_books = models.PositiveSmallIntegerField(default=2)
    send_message = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title


class Subscription(models.Model):
    from src.applications.users.models import User

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="subscription"
    )

    plan = models.ForeignKey(BillingPlan, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    expires_date = models.DateField()

    complete = models.BooleanField(default=False)
