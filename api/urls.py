from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r"genres", views.GenreViewSet)


urlpatterns = [
    path("", include(router.urls)),
    path("book_requests/", views.BookRequestAPIView.as_view()),
    path("book_relations/", views.BookRelationsAPIView.as_view()),
    path("book_relations/<int:id>/", views.DetailBookRelationsAPIView.as_view()),
]


urlpatterns += router.urls
