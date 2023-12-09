from rest_framework.routers import SimpleRouter
from django.urls import path
from . import views


router = SimpleRouter()

router.register(r"messages", viewset=views.PrivateMessageViewSet)

urlpatterns = []


urlpatterns += router.urls
