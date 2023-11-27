from http import HTTPStatus

from django.conf import settings
from django_filters import rest_framework as filter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView
from .permissions import IsOwnerOrStaff


from src.applications.users.models import User, UserEmailNewsLetter, UserFollowing
from src.applications.users.serializers import (
    EmailSerializer,
    NewsLetterSerializer,
    UserDetailSerializer,
    UserFollowingSerializer,
    UserSerializer,
)
from src.applications.users.tasks import send_message


class UsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = User.objects.all()
        email = self.request.query_params.get("email")
        ordering = self.request.query_params.get("ordering")
        if email is not None:
            queryset = User.objects.filter(email=email)
        if ordering is not None:
            queryset = queryset.order_by(ordering)
        serializer = UserSerializer(queryset, many=True)
        return Response({"user_list": serializer.data})


class DetailUserAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [permissions.IsAuthenticated]

    # def patch(self, request, user_id):
    #     user = User.objects.get(id=user_id)
    #     if request.user == user or user.is_superuser:
    #         user_data = UserDetailSerializer(data=request.data, instance=user)
    #         user_data.is_valid(raise_exception=True)
    #         user_data.save()
    #         return Response({"well_done": "OK"})
    #     return Response({"You dont have permission for this "})

    # def delete(self, request, user_id):
    #     user = User.objects.get(id=user_id)
    #     if request.user == user or request.user.is_superuser:
    #         user.delete()
    #         return Response({"delete": "object delete"})
    #     return Response({"You dont have permission for this "})

    def get_permissions(self):
        if self.request.method == "GET":
            return super().get_permissions()
        if self.request.method == "DELETE":
            return [permissions.IsAdminUser()]
        if self.request.method == "PATCH":
            return [IsOwnerOrStaff()]


class MyFollowersAPIView(ListAPIView):
    """Followers list"""

    queryset = UserFollowing.objects.all()
    serializer_class = UserFollowingSerializer

    def get(self, request):
        queryset = self.get_queryset().filter(user_id=request.user)
        serializer = self.serializer_class(instance=queryset, many=True)
        return Response({"my_followers": serializer.data})


class MyFollowingAPIView(APIView):
    """Subsctiption list"""

    def get(self, request):
        queryset = UserFollowing.objects.filter(followers_id=request.user)
        serializer = UserFollowingSerializer(instance=queryset, many=True)
        return Response({"my_followers": serializer.data})

    def post(self, request):
        serialazer = UserFollowingSerializer(data=request.data)
        serialazer.is_valid(raise_exception=True)
        serialazer.save(followers_id=request.user)
        return Response(status=200)


class SendEmailAPIView(APIView):
    def post(self, request):
        email = EmailSerializer(data=request.data)
        email.is_valid(raise_exception=True)
        message = request.data.get("message")
        subject = request.data.get("subject")
        to_user = request.data.get("to")
        send_message.delay(subject=subject, message=message, email=to_user)

        return Response({"email was sent!"}, status=HTTPStatus.CREATED)


class NewsLetterSettingsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset, _ = UserEmailNewsLetter.objects.get_or_create(user=request.user)
        serializer = NewsLetterSerializer(instance=queryset)
        return Response({"newsletter_settings": serializer.data})

    def patch(self, request):
        queryset, _ = UserEmailNewsLetter.objects.get_or_create(user=request.user)
        serializer = NewsLetterSerializer(data=request.data, instance=queryset)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"your newsletter": "was update"})
