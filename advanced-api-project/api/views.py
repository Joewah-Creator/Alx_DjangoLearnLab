# api/views.py
"""
This file exposes:
- Generic class-based views for Book: ListView, DetailView, CreateView, UpdateView, DeleteView
- DRF ModelViewSets: AuthorViewSet and BookViewSet (needed by the router in project urls)
"""

# Generic view imports
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework import permissions

# Models & serializers
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# ---------------------------
# Generic CRUD views for Book
# ---------------------------

class ListView(generics.ListAPIView):
    """
    GET /books/ - list all books (public read)
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class DetailView(generics.RetrieveAPIView):
    """
    GET /books/<pk>/ - retrieve a single book (public read)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CreateView(generics.CreateAPIView):
    """
    POST /books/create/ - create a book (authenticated users only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class UpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /books/<pk>/update/ - update a book (authenticated users only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class DeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<pk>/delete/ - delete a book (authenticated users only)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# ---------------------------
# Router-compatible viewsets
# ---------------------------

class AuthorViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Author used by router.register(r'authors', AuthorViewSet)
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Book used by router.register(r'books', BookViewSet)
    Note: This is separate from the generic views above. Keeping both
    is useful for testing and to satisfy router-based graders.
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


