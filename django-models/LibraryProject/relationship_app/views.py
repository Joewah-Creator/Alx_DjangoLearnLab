# django-models/relationship_app/views.py

from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from relationship_app.models import Book, Library

# Function-based view: list all books
def list_books(request):
    """
    Renders a list of all books with their authors.
    Uses context variable 'books' and template relationship_app/list_books.html
    """
    books = Book.objects.select_related('author').all()
    # If the caller prefers plain text instead of HTML, return HttpResponse with text.
    # But we'll render the provided template by default.
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: Library detail (includes library object + its books)
class LibraryDetailView(DetailView):
    """
    DetailView for Library model.
    Template: relationship_app/library_detail.html
    Context object name: 'library'
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    # Optionally override get_context_data to optimize queries
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Prefetch related books + their authors to minimize DB hits
        context['books'] = self.object.books.select_related('author').all()
        return context
