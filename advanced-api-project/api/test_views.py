# api/test_views.py
"""
Unit tests for Book API endpoints.

Covers:
- List and Detail reads (public access)
- Create / Update / Delete (authenticated only)
- Validation (publication_year not in the future)
- Filtering, searching and ordering on the list endpoint

Run with:
    python manage.py test api

Notes:
- Uses APIClient.force_authenticate to simulate an authenticated user.
- Assumes URL names in api/urls.py:
    'book-list', 'book-detail', 'book-create', 'book-update', 'book-delete'
  and that detail/update/delete expect a 'pk' kwarg.
"""

from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from datetime import date

from .models import Author, Book

User = get_user_model()

class BookAPITestCase(TestCase):
    def setUp(self):
        # Create a user for authenticated operations
        self.user = User.objects.create_user(username='tester', password='testpass')
        # API client instances
        self.client = APIClient()
        self.auth_client = APIClient()
        self.auth_client.force_authenticate(user=self.user)

        # Create an author
        self.author = Author.objects.create(name='Jane Doe')

        # Create sample books
        Book.objects.create(title='Alpha', publication_year=2000, author=self.author)
        Book.objects.create(title='Beta', publication_year=2010, author=self.author)
        Book.objects.create(title='Gamma', publication_year=2020, author=self.author)

    # -----------------------
    # Helper methods
    # -----------------------
    def _create_book_payload(self, title='New Book', year=None, author_id=None):
        if year is None:
            year = date.today().year
        if author_id is None:
            author_id = self.author.id
        return {'title': title, 'publication_year': year, 'author': author_id}

    # -----------------------
    # List & detail tests
    # -----------------------
    def test_list_books_public(self):
        """Anyone can list books (200 + correct count)."""
        url = reverse('book-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # We created 3 books in setUp
        self.assertEqual(len(resp.json()), 3)

    def test_retrieve_book_detail_public(self):
        """Anyone can retrieve book detail."""
        book = Book.objects.first()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.json()
        self.assertEqual(data['title'], book.title)
        self.assertEqual(data['publication_year'], book.publication_year)
        self.assertEqual(data['author'], book.author.id)

    # -----------------------
    # Create tests
    # -----------------------
    def test_create_book_unauthenticated_forbidden(self):
        """Unauthenticated users cannot create books (401/403)."""
        url = reverse('book-create')
        payload = self._create_book_payload()
        resp = self.client.post(url, payload, format='json')
        # depending on config this will be 401 Unauthorized or 403 Forbidden
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated_success(self):
        """Authenticated user can create a book and receives 201 with correct data."""
        url = reverse('book-create')
        payload = self._create_book_payload(title='Created by Auth', year=2015)
        resp = self.auth_client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        data = resp.json()
        self.assertEqual(data['title'], payload['title'])
        self.assertEqual(data['publication_year'], payload['publication_year'])
        self.assertEqual(data['author'], payload['author'])
        # DB contains the new book
        self.assertTrue(Book.objects.filter(title='Created by Auth').exists())

    def test_create_book_future_year_validation(self):
        """Creating a book with a future publication_year must fail with 400."""
        url = reverse('book-create')
        future_year = date.today().year + 10
        payload = self._create_book_payload(title='Future Book', year=future_year)
        resp = self.auth_client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        # Expect the error to mention publication_year
        self.assertIn('publication_year', resp.json())

    # -----------------------
    # Update tests
    # -----------------------
    def test_update_book_unauthenticated_forbidden(self):
        book = Book.objects.first()
        url = reverse('book-update', kwargs={'pk': book.pk})
        resp = self.client.patch(url, {'title': 'Hacked Title'}, format='json')
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated_success(self):
        book = Book.objects.first()
        url = reverse('book-update', kwargs={'pk': book.pk})
        new_title = 'Updated Title'
        resp = self.auth_client.patch(url, {'title': new_title}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, new_title)

    # -----------------------
    # Delete tests
    # -----------------------
    def test_delete_book_unauthenticated_forbidden(self):
        book = Book.objects.first()
        url = reverse('book-delete', kwargs={'pk': book.pk})
        resp = self.client.delete(url)
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_delete_book_authenticated_success(self):
        book = Book.objects.first()
        url = reverse('book-delete', kwargs={'pk': book.pk})
        resp = self.auth_client.delete(url)
        # Many setups return 204 NO CONTENT on delete
        self.assertIn(resp.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(pk=book.pk).exists())

    # -----------------------
    # Filtering / searching / ordering tests
    # -----------------------
    def test_filter_by_publication_year(self):
        url = reverse('book-list')
        resp = self.client.get(f"{url}?publication_year=2010")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.json()
        self.assertTrue(all(item['publication_year'] == 2010 for item in results))
        self.assertEqual(len(results), 1)

    def test_search_by_title_or_author_name(self):
        url = reverse('book-list')
        # search for 'Alpha' (title)
        resp = self.client.get(f"{url}?search=Alpha")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.json()
        self.assertTrue(any('Alpha' in item['title'] for item in results))

    def test_ordering_by_publication_year_desc(self):
        url = reverse('book-list')
        resp = self.client.get(f"{url}?ordering=-publication_year")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        results = resp.json()
        years = [item['publication_year'] for item in results]
        # Verify sorted descending
        self.assertEqual(years, sorted(years, reverse=True))
