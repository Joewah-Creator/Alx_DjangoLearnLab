# Alx_DjangoLearnLab/django-models/relationship_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .models import Book, Library, UserProfile, Author

# -----------------------
# Function-based view: list all books
# -----------------------
def list_books(request):
    books = Book.objects.all()
    try:
        return render(request, 'relationship_app/list_books.html', {'books': books})
    except Exception:
        lines = [f"{b.title} by {getattr(b.author, 'name', 'Unknown')}" for b in books]
        return HttpResponse("\n".join(lines), content_type='text/plain')


# -----------------------
# Class-based view: Library detail
# -----------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        library = ctx['library']
        # include books in context; try M2M then reverse FK
        try:
            books_qs = library.books.all()
        except Exception:
            books_qs = library.book_set.all()
        ctx['books'] = books_qs
        return ctx


# -----------------------
# Authentication / Registration
# -----------------------
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect(reverse_lazy('list_books'))
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'relationship_app/login.html'
    authentication_form = AuthenticationForm


class CustomLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'


# -----------------------
# Role-based helpers & views
# -----------------------
def is_admin(user):
    return getattr(getattr(user, 'userprofile', None), 'role', None) == 'Admin'

def is_librarian(user):
    return getattr(getattr(user, 'userprofile', None), 'role', None) == 'Librarian'

def is_member(user):
    return getattr(getattr(user, 'userprofile', None), 'role', None) == 'Member'


@login_required
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html', {'user': request.user})


@login_required
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html', {'user': request.user})


@login_required
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html', {'user': request.user})


# -----------------------
# Book CRUD views protected by permissions
# -----------------------
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    """
    Minimal add-book view: GET renders simple form, POST creates Book.
    Expects: POST 'title' and 'author_id'
    """
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author_id = request.POST.get('author_id')
        if not title or not author_id:
            return HttpResponse("Missing title or author_id", status=400)
        author = get_object_or_404(Author, pk=author_id)
        Book.objects.create(title=title, author=author)
        return redirect('list_books')
    authors = Author.objects.all()
    return render(request, 'relationship_app/add_book.html', {'authors': authors})


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    """
    Minimal edit-book view: GET renders form, POST updates book.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        author_id = request.POST.get('author_id')
        if not title or not author_id:
            return HttpResponse("Missing title or author_id", status=400)
        author = get_object_or_404(Author, pk=author_id)
        book.title = title
        book.author = author
        book.save()
        return redirect('list_books')
    authors = Author.objects.all()
    return render(request, 'relationship_app/edit_book.html', {'book': book, 'authors': authors})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    """
    Minimal delete-book view: POST deletes and redirects. GET shows confirmation.
    """
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})

