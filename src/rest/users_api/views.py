from http import HTTPStatus

from django.conf import settings
from django_filters import rest_framework as filter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from src.applications.users.models import User, UserEmailNewsLetter, UserFollowing
from src.applications.users.serializers import (
    EmailSerializer,
    NewsLetterSerializer,
    FollowingSerializer,
    UserListSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    FollowersListSerializer,
    ChangeNewsLetterSerializer,
)
from src.applications.users.tasks import send_message

from .permissions import IsOwnerOrStaff


class UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing users, avalilable only for staff users.

    list:
    Returns a list of all users.
    Can be filtered by 'is_staff' and searched by 'email' or 'full_name'.

    retrieve:
    Returns the details of a specific user.

    partial_update:
    Updates a user's information.

    Parameters:
    - is_staff (bool): Choose true or false to filter users by staff status.
    - email (str): Search users by email.

    """

    queryset = User.objects.all()
    serializer_class = UserListSerializer
    http_method_names = ["get", "patch", "delete"]
    permission_classes = [IsAdminUser]
    filter_backends = [filter.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ["is_staff"]
    search_fields = ["email", "full_name"]

    @swagger_auto_schema(
        operation_description="test",
        manual_parameters=[
            openapi.Parameter(
                "is_staff",
                in_=openapi.IN_QUERY,
                description="Choose true or false",
                required=False,
                type=openapi.TYPE_BOOLEAN,
            ),
        ],
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.action == "list":
            return super().get_serializer_class()

        if self.action == "retrieve":
            return UserDetailSerializer

        if self.action == "partial_update":
            return UserUpdateSerializer


class FollowersViewSet(viewsets.GenericViewSet):
    """
    API endpoint for managing user followers and subscriptions.

    followers_list:
        returns the list of users to which this current user is subscribed.

    subscription_list:
        returns the list of users who are subscribed to this current user.

    follow_action:
        subscription and unsubscribe action for a specific user.

    """

    queryset = UserFollowing.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = FollowersListSerializer

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="my-followers",
    )
    def followers_list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(user_id=self.request.user)
        serializer = FollowersListSerializer(instance=queryset, many=True)
        return Response({"followers_list": serializer.data})

    @action(
        methods=["get"],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path="my-subscription",
    )
    def subscription_list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(followers_id=self.request.user)
        serializer = FollowersListSerializer(instance=queryset, many=True)
        return Response({"suscription_list": serializer.data})

    @action(
        methods=["post"],
        detail=False,
        url_path="subscript-to",
        permission_classes=[IsAuthenticated],
    )
    def follow_action(self, request, *args, **kwargs):
        data = FollowingSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        data.save(followers_id=request.user)

        return Response(status=200)


class SendEmailAPIView(APIView):
    """
    - Endpoint for sending emails.
    - Only authorized user can send mails.
    - It is not possible to send a letter to yourself and to an e-mail that is not registered on the site.

    """

    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=EmailSerializer,
        operation_description="Send email between users",
    )
    def post(self, request):
        email = EmailSerializer(data=request.data)
        email.is_valid(raise_exception=True)
        message = email.validated_data.get("message")
        subject = email.validated_data.get("subject")
        to_user = email.validated_data.get("to")
        send_message.delay(subject=subject, message=message, email=to_user)

        return Response(status=HTTPStatus.CREATED)


class NewsLetterSettingsViewSet(viewsets.GenericViewSet):
    """
    ViewSet for managing email newsletter settings.

    """

    queryset = UserEmailNewsLetter.objects.all()
    permission_classes = [IsAuthenticated]

    @action(methods=["get"], detail=False, url_path="my-newsletter")
    def my_newsletter(self, request, *args, **kwargs):
        """
        Get email newsletter settings for the current user.
        """
        queryset, _ = UserEmailNewsLetter.objects.get_or_create(user=request.user)
        serializer = NewsLetterSerializer(instance=queryset, many=False)

        return Response({"user_news_letter": serializer.data})

    @swagger_auto_schema(
        method="get", operation_description="list of users newsletter settings"
    )
    @action(
        methods=["get"],
        detail=False,
        url_path="admin/newletter-list",
        permission_classes=[IsAdminUser],
    )
    def nawsletter_list(self, request):
        """
        Get a list of email newsletter settings for administrators.
        Available only for staff users.
        """
        serializer = NewsLetterSerializer(self.get_queryset(), many=True)
        return Response({"newsletter_list": serializer.data})

    @swagger_auto_schema(
        method="patch",
        request_body=ChangeNewsLetterSerializer,
        operation_description="change newsletter settings",
    )
    @action(
        methods=["patch"],
        detail=False,
        url_path="change-newletter",
        permission_classes=[IsOwnerOrStaff],
    )
    def change_newsletter(self, request, *args, **kwargs):
        """
        Change email newsletter settings for the current user.
        """
        newsletter, _ = UserEmailNewsLetter.objects.update_or_create(user=request.user)

        serializer = ChangeNewsLetterSerializer(
            instance=newsletter, data=request.data, many=False
        )

        serializer.is_valid(raise_exception=True)

        for field, value in serializer.validated_data.items():
            newsletter.__setattr__(field, value)

        newsletter.save()

        return Response(data="Settings was updated", status=200)

    def get_permissions_classes(self):
        """
        Define permission classes based on the action.
        """

        if self.action == "list":
            return IsAdminUser
        return super().get_permissions()
