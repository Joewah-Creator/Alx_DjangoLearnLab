from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library

# ---- Function-based view: list all books ----
def list_books(request):
    """
    Lists all books. If a template 'relationship_app/list_books.html' is present
    it will render that; otherwise returns a plain text list.
    """
    books = Book.objects.select_related('author').all()

    # Try template if available
    try:
        # Render template (optional)
        return render(request, 'relationship_app/list_books.html', {'books': books})
    except Exception:
        # Fallback to plain text
        lines = [f"{b.title} by {getattr(b.author, 'name', 'Unknown')}" for b in books]
        return HttpResponse("\n".join(lines), content_type='text/plain')


# ---- Class-based view: show library detail + its books ----
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'  # optional template

    # context_object_name will make the template use "library"
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        library = ctx['library']

        # Try common access patterns for related books:
        # 1) library.books.all() (ManyToMany or related_name)
        # 2) library.book_set.all() (default reverse FK)
        try:
            books_qs = library.books.all()
        except Exception:
            # fallback to reverse FK
            books_qs = getattr(library, 'book_set', Book.objects.none()).all()

        # Use select_related for author where possible
        books_qs = books_qs.select_related('author') if hasattr(books_qs, 'select_related') else books_qs

        ctx['books'] = books_qs
        return ctx

