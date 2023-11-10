from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()


urlpatterns = [
    path("", include(router.urls)),
    path("book_requests/", views.BookRequestAPIView.as_view()),
]


urlpatterns += router.urls
