from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django_email_verification import urls as email_urls

app_pattern = "src.applications."
rest_pattern = "src.rest."

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    # djoser
    path("api/auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    # api apps
    path("api-users/", include(f"{rest_pattern}users_api.urls")),
    # email verification
    path("email/", include(email_urls)),
    # books apps
    path("", include(f"{app_pattern}books.urls")),
    # users apps
    path("users/", include(f"{app_pattern}users.urls")),
    path("api-books/", include(f"{rest_pattern}books_api.urls")),
    # allauth
    path("accounts/", include("allauth.urls")),
    # book-relations apps
    path("", include(f"{app_pattern}book_relations.urls")),
    path("api-books-relations/", include(f"{rest_pattern}book_relations_api.urls")),
    # book-requests apps
    path("", include(f"{app_pattern}book_requests.urls")),
    path("api-books-requests/", include(f"{rest_pattern}book_requests_api.urls")),
    # chat apps
    path("chat/", include(f"{app_pattern}chat.urls")),
    path("api-chat/", include(f"{rest_pattern}chat_api.urls")),
    # gallery app
    path("gallery/", include(f"{app_pattern}gallery.urls")),
    # news app
    path("news/", include(f"{app_pattern}news.urls")),
    #
    path("subscriptions/", include(f"{app_pattern}subscriptions.urls")),
    path("api-subscriptions/", include(f"{rest_pattern}subscriptions_api.urls")),
    #
    # debug toolbar
    path("__debug__/", include("debug_toolbar.urls")),
    # captcha
    path("captcha/", include("captcha.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Custom admin

admin.site.index_title = "Book Change Application"

admin.site.site_header = "Admin Area"
