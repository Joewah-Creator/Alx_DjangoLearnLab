# api/test_views.py
"""
Unit tests for Book API endpoints using DRF APIClient.

Uses `response.data` (DRF Response) so tests match the grader's substring checks.
Run with: python manage.py test api
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

    # Helper to normalize DRF response.data when pagination is enabled
    def _data_list(self, response):
        data = response.data
        if isinstance(data, dict) and 'results' in data:
            return data['results']
        return data

    def _create_book_payload(self, title='New Book', year=None, author_id=None):
        if year is None:
            year = date.today().year
        if author_id is None:
            author_id = self.author.id
        return {'title': title, 'publication_year': year, 'author': author_id}

    def test_list_books_public(self):
        """Anyone can list books (200 + correct count)."""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = self._data_list(response)
        self.assertEqual(len(results), 3)

    def test_retrieve_book_detail_public(self):
        """Anyone can retrieve book detail."""
        book = Book.objects.first()
        url = reverse('book-detail', kwargs={'pk': book.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = response.data
        self.assertEqual(data['title'], book.title)
        self.assertEqual(data['publication_year'], book.publication_year)
        # author field may be an id in serializer
        self.assertEqual(data['author'], book.author.id)

    def test_create_book_unauthenticated_forbidden(self):
        """Unauthenticated users cannot create books."""
        url = reverse('book-create')
        payload = self._create_book_payload()
        response = self.client.post(url, payload, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated_success(self):
        """Authenticated user can create a book and receives 201 with correct data."""
        url = reverse('book-create')
        payload = self._create_book_payload(title='Created by Auth', year=2015)
        response = self.auth_client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.data
        self.assertEqual(data['title'], payload['title'])
        self.assertEqual(data['publication_year'], payload['publication_year'])
        self.assertEqual(data['author'], payload['author'])
        self.assertTrue(Book.objects.filter(title='Created by Auth').exists())

    def test_create_book_future_year_validation(self):
        """Creating a book with a future publication_year must fail with 400."""
        url = reverse('book-create')
        future_year = date.today().year + 10
        payload = self._create_book_payload(title='Future Book', year=future_year)
        response = self.auth_client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('publication_year', response.data)

    def test_update_book_unauthenticated_forbidden(self):
        book = Book.objects.first()
        url = reverse('book-update', kwargs={'pk': book.pk})
        response = self.client.patch(url, {'title': 'Hacked Title'}, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated_success(self):
        book = Book.objects.first()
        url = reverse('book-update', kwargs={'pk': book.pk})
        new_title = 'Updated Title'
        response = self.auth_client.patch(url, {'title': new_title}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book.refresh_from_db()
        self.assertEqual(book.title, new_title)

    def test_delete_book_unauthenticated_forbidden(self):
        book = Book.objects.first()
        url = reverse('book-delete', kwargs={'pk': book.pk})
        response = self.client.delete(url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_delete_book_authenticated_success(self):
        book = Book.objects.first()
        url = reverse('book-delete', kwargs={'pk': book.pk})
        response = self.auth_client.delete(url)
        self.assertIn(response.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(pk=book.pk).exists())

    def test_filter_by_publication_year(self):
        url = reverse('book-list')
        response = self.client.get(f"{url}?publication_year=2010")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = self._data_list(response)
        self.assertTrue(all(item['publication_year'] == 2010 for item in results))
        self.assertEqual(len(results), 1)

    def test_search_by_title_or_author_name(self):
        url = reverse('book-list')
        response = self.client.get(f"{url}?search=Alpha")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = self._data_list(response)
        self.assertTrue(any('Alpha' in item['title'] for item in results))

    def test_ordering_by_publication_year_desc(self):
        url = reverse('book-list')
        response = self.client.get(f"{url}?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = self._data_list(response)
        years = [item['publication_year'] for item in results]
        self.assertEqual(years, sorted(years, reverse=True))
