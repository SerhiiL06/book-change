from django.urls import path, include
from rest_framework.routers import SimpleRouter
from . import views


router = SimpleRouter()
router.register(r"users", views.UserViewSet)


urlpatterns = [
    path("", include(router.urls)),
]


urlpatterns += router.urls
