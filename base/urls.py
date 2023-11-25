from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django_email_verification import urls as email_urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api-auth/", include("rest_framework.urls")),
    # djoser
    path("api/auth/", include("djoser.urls")),
    re_path(r"^auth/", include("djoser.urls.authtoken")),
    # api apps
    path("api-users/", include("users_api.urls")),
    # email verification
    path("email/", include(email_urls)),
    # books apps
    path("", include("books.urls")),
    # users apps
    path("users/", include("users.urls")),
    path("api-books/", include("books_api.urls")),
    # allauth
    path("accounts/", include("allauth.urls")),
    # book-relations apps
    path("", include("book_relations.urls")),
    path("api-books-relations/", include("book_relations_api.urls")),
    # book-requests apps
    path("", include("book_requests.urls")),
    path("api-books-requests/", include("book_requests_api.urls")),
    # chat apps
    path("chat/", include("chat.urls")),
    path("api-chat/", include("chat_api.urls")),
    # gallery app
    path("gallery/", include("gallery.urls")),
    # news app
    path("news/", include("news.urls")),
    #
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
