from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus
from django.contrib.auth import get_user_model


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
        self.data = data
        user = get_user_model().objects.create(email=data.get("email"))
        user.set_password(data.get("password1"))
        user.is_active = True
        user.save()
        self.user = user

    def test_login(self):
        path = reverse("users:login")
        response = self.client.post(path=path, data=self.data)

        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse("books:index"))

        self.assertTrue(self.user.is_authenticated)
