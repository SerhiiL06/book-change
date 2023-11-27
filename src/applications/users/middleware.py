from django.utils import timezone


class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            request.user.last_activity = timezone.now()
            request.user.status = "online"
            request.user.save()

        response = self.get_response(request)
        return response
