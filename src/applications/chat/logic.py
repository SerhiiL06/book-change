from .models import PrivateMessage


def get_unique(request, position, value):
    if position == "sender":
        filtering_fields = {"sender": request.user}
    if position == "recipient":
        filtering_fields = {"recipient": request.user}
    unique_recipients = (
        PrivateMessage.objects.filter(**filtering_fields)
        .values_list(value, flat=True)
        .distinct()
    )
    return unique_recipients
