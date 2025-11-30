# api/views.py
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

class ListView(generics.ListAPIView):
    """
    GET /books/ - list all books (readable by anyone).
    Uses IsAuthenticatedOrReadOnly so read access is public but mutating actions
    require authentication if this class were to be reused for such actions.
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class DetailView(generics.RetrieveAPIView):
    """
    GET /books/<pk>/ - retrieve a single book (readable by anyone).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CreateView(generics.CreateAPIView):
    """
    POST /books/create/ - create a book (authenticated users only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class UpdateView(generics.UpdateAPIView):
    """
    PUT/PATCH /books/<pk>/update/ - update a book (authenticated users only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

class DeleteView(generics.DestroyAPIView):
    """
    DELETE /books/<pk>/delete/ - delete a book (authenticated users only).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

