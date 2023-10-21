from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as email_urls
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("email/", include(email_urls)),
    path("", include("books.urls")),
    path("users/", include("users.urls")),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
