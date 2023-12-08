from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register("admin/users", views.UsersViewSet)
router.register("followers", views.FollowersViewSet)
router.register("news_letter", views.NewsLetterSettingsViewSet)


urlpatterns = [
    path("send-email/", views.SendEmailAPIView.as_view()),
]


urlpatterns += router.urls
