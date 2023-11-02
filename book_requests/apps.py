from django.apps import AppConfig


class BookRequestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "book_requests"

    def ready(self):
        import book_requests.signals
