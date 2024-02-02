from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase


class UserAdminTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = get_user_model().objects.create(
            email="userfortest@gmail.com",
            password="TheTestPassword",
            is_staff=True,
            is_active=True,
        )

    def test_get_user_admin_endpoint(self):
        path = reverse("users_api:user-admin-list")
        response = self.client.get(path)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.client.login(email="userfortest@gmail.com", password="TheTestPassword")

        self.assertEqual(get_user_model().objects.count(), 1)

        response = self.client.get(path)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
