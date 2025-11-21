# api/views.py
from rest_framework import generics, viewsets
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    Existing read-only list view (keeps earlier functionality).
    GET /api/books/ -> list books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    Full CRUD for Book.
    - list:   GET  /api/books_all/
    - retrieve: GET /api/books_all/<pk>/
    - create: POST /api/books_all/
    - update: PUT /api/books_all/<pk>/
    - partial_update: PATCH /api/books_all/<pk>/
    - destroy: DELETE /api/books_all/<pk>/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

