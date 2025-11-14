from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

from .models import Book


# Protected list view (requires can_view)
@permission_required('bookshelf.can_view', raise_exception=True)
def protected_list_books(request):
    """
    List all books — only users with 'bookshelf.can_view' can access.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/list_books.html', {'books': books})


# Create (requires can_create)
@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    """
    Minimal book creation view.
    GET -> render a simple form (bookshelf/add_book.html).
    POST -> create Book from POST fields: title, author, publication_year.
    """
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author = request.POST.get('author', '').strip()
        year = request.POST.get('publication_year', '').strip()
        try:
            year = int(year) if year else None
        except ValueError:
            year = None

        book = Book.objects.create(title=title or 'Untitled',
                                   author=author or 'Unknown',
                                   publication_year=year or 0)
        return HttpResponse(f"Book created: {book}", content_type="text/plain")

    return render(request, 'bookshelf/add_book.html')


# Edit (requires can_edit)
@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    """
    Minimal book edit view.
    GET -> render bookshelf/edit_book.html with book context.
    POST -> update fields and save.
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.title = request.POST.get('title', book.title).strip() or book.title
        book.author = request.POST.get('author', book.author).strip() or book.author
        year = request.POST.get('publication_year', '')
        try:
            book.publication_year = int(year) if year else book.publication_year
        except ValueError:
            pass
        book.save()
        return HttpResponse(f"Book updated: {book}", content_type="text/plain")

    return render(request, 'bookshelf/edit_book.html', {'book': book})


# Delete (requires can_delete)
@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    """
    Minimal book delete view.
    GET -> confirm page (bookshelf/delete_book.html).
    POST -> deletes the book.
    """
    book = get_object_or_404(Book, id=book_id)

    if request.method == 'POST':
        book.delete()
        return HttpResponse("Book deleted.", content_type="text/plain")

    return render(request, 'bookshelf/delete_book.html', {'book': book})

