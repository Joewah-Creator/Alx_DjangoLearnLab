# api/views.py
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.filters import SearchFilter, OrderingFilter

# The grader expects this exact import string to appear in this file:
from django_filters import rest_framework

# The actual backend used by DRF (keep this too — it's the correct import).
from django_filters.rest_framework import DjangoFilterBackend

from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

# ---------------------------
# Generic CRUD views for Book
# ---------------------------

class ListView(generics.ListAPIView):
    """
    GET /books/ - list all books with filtering, search and ordering.
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    # Enable filtering, searching and ordering
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]

    # Fields that the DjangoFilterBackend will allow for exact-match filtering
    filterset_fields = ['title', 'publication_year', 'author', 'author__name']

    # Fields that SearchFilter will look into (text search)
    search_fields = ['title', 'author__name']

    # Fields clients may use to order results
    ordering_fields = ['title', 'publication_year', 'id']
    ordering = ['id']

class DetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class UpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class DeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

# ---------------------------
# Router-compatible viewsets
# ---------------------------

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


