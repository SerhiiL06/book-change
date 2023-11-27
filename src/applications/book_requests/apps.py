from django.apps import AppConfig


class BookRequestsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.applications.book_requests"

    def ready(self):
        import src.applications.book_requests.signals
