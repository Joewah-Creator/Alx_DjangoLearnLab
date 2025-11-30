# api/generic_views.py
"""
Generic views for Book using Django REST Framework generics.

Views provided:
- BookListAPIView    : GET    /api/books/          -> list all books (readable by anyone)
- BookDetailAPIView  : GET    /api/books/<pk>/     -> retrieve a single book (readable by anyone)
- BookCreateAPIView  : POST   /api/books/create/   -> create (authenticated only)
- BookUpdateAPIView  : PUT/PATCH /api/books/<pk>/update/ -> update (authenticated only)
- BookDeleteAPIView  : DELETE /api/books/<pk>/delete/ -> delete (authenticated only)

Permissions:
- Read views: AllowAny
- Mutating views: IsAuthenticated

Customization:
- BookCreateAPIView and BookUpdateAPIView will call serializer.is_valid(raise_exception=True)
  to enforce validation and return standard DRF errors when validation fails.
- You can add filtering, ordering or pagination as needed.
"""
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer

# Read-only list view
class BookListAPIView(generics.ListAPIView):
    """
    Returns a paginated list of all Book objects.
    Accessible to unauthenticated users (AllowAny).
    """
    queryset = Book.objects.all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# Read-only detail view
class BookDetailAPIView(generics.RetrieveAPIView):
    """
    Returns the details of a single Book identified by pk.
    Accessible to unauthenticated users (AllowAny).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]

# Create view (authenticated users only)
class BookCreateAPIView(generics.CreateAPIView):
    """
    Create a new Book.
    Only authenticated users can create.
    Uses serializer validation (publication_year validation lives in the serializer).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    # CreateAPIView already calls serializer.is_valid() and serializer.save(),
    # but we can override perform_create if extra logic is needed.
    # def perform_create(self, serializer):
    #     serializer.save(created_by=self.request.user)  # example

# Update view (authenticated users only)
class BookUpdateAPIView(generics.UpdateAPIView):
    """
    Update an existing Book (PUT or PATCH).
    Only authenticated users may update.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

# Delete view (authenticated users only)
class BookDeleteAPIView(generics.DestroyAPIView):
    """
    Delete an existing Book (DELETE).
    Only authenticated users may delete.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
