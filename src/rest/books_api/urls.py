from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()

router.register(r"genre", views.GenreViewSets)
router.register(r"author", views.AuthorViewSet)
router.register(r"book", views.BookViewSet)
router.register(r"comment", views.CommentViewSet)


urlpatterns = []


urlpatterns += router.urls
