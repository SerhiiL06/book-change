from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as email_urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    path("api/", include("api.urls")),
    path("email/", include(email_urls)),
    path("", include("books.urls")),
    path("users/", include("users.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Custom admin

admin.site.index_title = "Book Change Application"

admin.site.site_header = "Admin Area"
