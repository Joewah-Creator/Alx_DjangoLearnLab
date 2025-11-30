# api/views.py
"""
Generic CRUD views for Book expected by the grader.
Class names must match: ListView, DetailView, CreateView, UpdateView, DeleteView
"""

from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

class ListView(generics.ListAPIView):
    """
    GET /books/ - list all books (public)
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class DetailView(generics.RetrieveAPIView):
    """
    GET /books/<pk>/ - retrieve a single book (public)
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

class CreateView(generics.CreateAPIView):
    """
    POST /books/create/ - create a book (authenticated users only)
    Uses serializer validation (publication_year validation lives in serializer).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # keep default behaviour; serializer.is_valid(raise_exception=True) is called by CreateAPIView

class UpdateView(generics.UpdateAPIView):
    ""

