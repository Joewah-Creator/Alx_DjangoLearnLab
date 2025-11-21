# api/views.py
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    GET /api/books/ -> returns a JSON list of Book instances
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
