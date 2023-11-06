from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r"users", views.UserViewSet)
router.register(r"genres", views.GenreViewSet)
router.register(r"books", views.BookViewSet)


urlpatterns = [
    path("", include(router.urls)),
]


urlpatterns += router.urls
