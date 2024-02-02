from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from src.applications.news.models import Like, News
from src.applications.news.serializers import NewsSerializer


class NewsViewset(viewsets.ModelViewSet):
    queryset = News.objects.prefetch_related("author")
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = NewsSerializer
    http_method_names = ["get", "delete", "post"]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=["POST"], detail=True, url_path="like")
    def like_news(self, request, pk: int):
        news = get_object_or_404(News, id=pk)
        like_cheker, create = Like.objects.get_or_create(user=request.user, news=news)

        if create:
            news.likes += 1
        else:
            like_cheker.delete()
            news.likes -= 1
        news.save()

        return Response({"message": "SUCCESS"}, status.HTTP_200_OK)
