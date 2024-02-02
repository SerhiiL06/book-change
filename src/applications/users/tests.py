from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import User


class RegisterTestCase(TestCase):
    def test_register(self):
        data = {
            "email": "example@gmail.com",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
        }

        wrong_data = data.copy()
        wrong_data["password2"] = "TestPassword122"

        users = get_user_model().objects.all()

        # create user with incorrect data
        wrong_response = self.client.post(reverse("users:register"), wrong_data)
        self.assertEqual(wrong_response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(wrong_response, reverse("users:register"))
        self.assertEqual(users.count(), 0)

        # create user with correct data
        response = self.client.post(reverse("users:register"), data)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("users:email-verification-sent"))
        self.assertEqual(users.count(), 1)

        # check email
        self.assertEqual(users.last().email, data.get("email"))


class LoginTestCase(TestCase):
    def setUp(self):
        data = {
            "email": "example@gmail.com",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
        }
        self.user = User.objects.create_superuser(
            email=data["email"], password=data["password1"]
        )

    def test_login(self):
        # check login
        client = Client()
        status = client.login(email="example@gmail.com", password="TestPassword123")
        self.assertTrue(status)

        # check statuses in get request
        path = reverse("users:login")

        response = self.client.get(path)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "users/login/login.html")

        # check logout

        path_logout = reverse("users:logout")

        logout_response = self.client.get(path_logout)

        self.assertEqual(logout_response.status_code, 302)


class ProfileTestCase(TestCase):
    def setUp(self):
        data = {
            "email": "example@gmail.com",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
        }
        self.data = data
        self.user = User.objects.create_superuser(
            email=data["email"], password=data["password1"]
        )

    def test_update_profile(self):
        pass

    def test_get_options_page(self):
        client = Client()
        login = client.login(email="example@gmail.com", password="TestPassword123")

        self.assertTrue(login)

        path = reverse("users:options")

        response = self.client.get(path)

        self.assertTemplateUsed(response, "users/user-options.html")

        self.assertEqual(response.status_code, 200)
