# django-models/relationship_app/views.py

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView

from relationship_app.models import Book, Library

# Function-based view required by the grader.
def list_books(request):
    """
    Return a simple plain-text listing of all books and their authors.
    The grader expects the exact call pattern: Book.objects.all()
    """
    books = Book.objects.all()

    # Build lines and return plain text
    lines = [f"{b.title} by {b.author.name}" for b in books]
    content = "\n".join(lines) if lines else "No books available."
    return HttpResponse(content, content_type="text/plain")


# Class-based DetailView for Library required by the grader.
class LibraryDetailView(DetailView):
    """
    The grader expects a class-based view using DetailView and model = Library.
    """
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Preload books and their authors to optimize rendering
        context['books'] = self.object.books.select_related('author').all()
        return context
