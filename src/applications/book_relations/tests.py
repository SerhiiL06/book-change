from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from src.applications.books.models import Author, Book

from .models import BookRelations


class BookRelationsTestCase(TestCase):
    def setUp(self):
        author = Author.objects.create(name="TestName", country="UA")
        self.user = get_user_model().objects.create_superuser(
            email="example@gmail.com", password="TestPass123"
        )

        self.book = Book.objects.create(
            title="Test Title", author=author, owner=self.user
        )

    def test_add_to_bookmark(self):
        current_client = Client()

        current_client.login(email="example@gmail.com", password="TestPass123")
        path = reverse(
            "book_relations:add-to-bookmark", kwargs={"book_slug": "test-title"}
        )

        response = current_client.get(path)

        # check bookmark get response
        self.book.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("books:index"))
        # check if bookmark will be saved
        self.assertEqual(self.book.book_relation.get(user=self.user).bookmark, True)

    def test_left_rating(self):
        current_client = Client()
        current_client.login(email="example@gmail.com", password="TestPass123")

        path = reverse("book_relations:rating")

        current_client.post(path, data={"book_id": self.book.id, "rating": 5})

        # check rating system

        self.book.refresh_from_db()

        # test if rating will be saved
        self.assertEqual(self.book.book_relation.get(user=self.user).rating, 5)

        # test user bookmark list get request
        bookmark_list = reverse("book_relations:bookmark-list")

        response = current_client.get(bookmark_list)

        self.assertEqual(response.status_code, 200)

        # test if bookmark will be saved in db
        self.assertEqual(
            BookRelations.objects.filter(user=self.user, book=self.book).count(), 1
        )
