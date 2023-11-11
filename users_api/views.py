from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filter
from users.tasks import send_message
from .permissions import IsAuthenticatedAndOwner
from http import HTTPStatus
from django.conf import settings
from users.models import User, UserFollowing
from users.serializers import (
    UserSerializer,
    UserDetailSerializer,
    EmailSerializer,
    UserFollowingSerializer,
)


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


class DetailUserAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAuthenticatedAndOwner]

    def get(self, request, user_id):
        try:
            queryset = User.objects.get(id=user_id)
        except:
            return Response({"error": "user dont exist"})

        serializer = UserDetailSerializer(queryset, many=False)
        return Response({"user_list": serializer.data})

    def patch(self, request, user_id):
        user = User.objects.get(id=user_id)
        if request.user == user or user.is_superuser:
            user_data = UserDetailSerializer(data=request.data, instance=user)
            user_data.is_valid(raise_exception=True)
            user_data.save()
            return Response({"well_done": "OK"})
        return Response({"You dont have permission for this "})

    def delete(self, request, user_id):
        user = User.objects.get(id=user_id)
        if request.user == user or request.user.is_superuser:
            user.delete()
            return Response({"delete": "object delete"})
        return Response({"You dont have permission for this "})


class MyFollowersAPIView(APIView):
    """Followers list"""

    def get(self, request):
        queryset = UserFollowing.objects.filter(user_id=request.user)
        serializer = UserFollowingSerializer(instance=queryset, many=True)
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
