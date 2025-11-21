# api/views.py
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    Public read-only endpoint.
    Anyone can GET /api/books/
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    """
    Full CRUD endpoint secured by token authentication.
    Requires a valid token for:
    - POST
    - PUT / PATCH
    - DELETE
    List & retrieve require authentication as per global settings.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Override permissions if you want stricter rules
    permission_classes = [IsAuthenticated]
    # Use this instead if only admins should edit:
    # permission_classes = [IsAdminUser]

