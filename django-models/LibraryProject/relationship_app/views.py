from .models import Book, Library
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import DetailView
from .models import Book, Library  

def list_books(request):
    books = Book.objects.all()
    try:
        return render(request, 'relationship_app/list_books.html', {'books': books})
    except Exception:
        lines = [f"{b.title} by {getattr(b.author, 'name', 'Unknown')}" for b in books]
        return HttpResponse("\n".join(lines), content_type='text/plain')


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        library = ctx['library']
        try:
            books_qs = library.books.all()
        except Exception:
            books_qs = library.book_set.all()
        ctx['books'] = books_qs
        return ctx

