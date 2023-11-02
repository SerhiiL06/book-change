from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import HistoryRequests
from datetime import timedelta
from django.utils import timezone


@receiver(post_save, sender=HistoryRequests)
def cleanup_history(**kwargs):
    """Delete history almost 30 days"""
    one_mounth_ago = timezone.now() - timedelta(days=30)
    HistoryRequests.objects.filter(create_at__lt=one_mounth_ago).delete()
