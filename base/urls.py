from django.contrib import admin
from django.urls import path, include, re_path
from django_email_verification import urls as email_urls
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    # djoser
    path("api/auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    # api app
    path("api/", include("api.urls")),
    # email verification
    path("email/", include(email_urls)),
    # books app
    path("", include("books.urls")),
    # users app
    path("users/", include("users.urls")),
    # book-relations app
    path("", include("book_relations.urls")),
    path("", include("book_requests.urls")),
    #
    #
    # debug toolbar
    path("__debug__/", include("debug_toolbar.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Custom admin

admin.site.index_title = "Book Change Application"

admin.site.site_header = "Admin Area"
