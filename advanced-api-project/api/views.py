# api/views.py
from rest_framework import viewsets
from .models import Author, Book
from .serializers import AuthorSerializer, BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    """
    Simple ModelViewSet for Author. Uses AuthorSerializer which nests related books.
    """
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class BookViewSet(viewsets.ModelViewSet):
    """
    Simple ModelViewSet for Book. Uses BookSerializer which validates publication_year.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

