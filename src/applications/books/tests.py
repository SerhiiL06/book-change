from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from src.applications.users.models import User

from .models import Author, Book


class BookPageTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_superuser(
            email="test@gmail.com", password="TestPassword123"
        )
        author = Author.objects.create(name="Test", country="UA")
        Book.objects.create(title="Test Books1", owner=user, author=author)
        Book.objects.create(title="Test Books2", owner=user, author=author)
        Book.objects.create(title="Test Books3", owner=user, author=author)

    def test_index_page(self):
        path = reverse("books:index")
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertTemplateUsed(response, "index.html")

        self.assertEqual(len(Book.objects.all()), 3)

        self.assertEqual(len(response.context["object_list"]), 3)

    def test_book_detail(self):
        path = reverse("books:detail-book", kwargs={"slug": "test-books1"})
        response = self.client.get(path)

        self.assertEqual(response.status_code, HTTPStatus.OK)

        self.assertTemplateUsed(response, "books/book-detail.html")

        self.assertEqual(response.context["object"], Book.objects.get(id=1))
