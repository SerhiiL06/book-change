from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings


schema_view = get_schema_view(
    openapi.Info(
        title="Book-change API",
        default_version="v1",
        description="Book change service",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(settings.EMAIL_HOST_USER),
        license=openapi.License(name="Serhii License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path(
        "swagger<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
