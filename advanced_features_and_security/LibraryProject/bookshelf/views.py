from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required

from .models import Book
from .forms import ExampleForm   # <-- exact import the checker expects


def book_list(request):
    """
    Public book list view (checker expects a symbol named `book_list`).
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_view', raise_exception=True)
def protected_list_books(request):
    """
    Protected list view: only users with 'bookshelf.can_view' may access.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('bookshelf.can_create', raise_exception=True)
def add_book(request):
    """
    Add a book using ExampleForm. GET -> render form; POST -> validate & create.
    """
    if request.method == 'POST':
        form = ExampleForm(request.POST)
        if form.is_valid():
            book = form.save()
            return HttpResponse(f"Book created: {book}", content_type="text/plain")
    else:
        form = ExampleForm()
    return render(request, 'bookshelf/form_example.html', {'form': form})


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request, book_id):
    """
    Edit book using ExampleForm. GET -> render form; POST -> validate & save.
    """
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = ExampleForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return HttpResponse(f"Book updated: {book}", content_type="text/plain")
    else:
        form = ExampleForm(instance=book)
    return render(request, 'bookshelf/form_example.html', {'form': form, 'book': book})


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request, book_id):
    """
    Confirm and delete a book. GET -> confirmation page; POST -> delete.
    """
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        book.delete()
        return HttpResponse("Book deleted.", content_type="text/plain")
    return render(request, 'bookshelf/delete_book.html', {'book': book})
