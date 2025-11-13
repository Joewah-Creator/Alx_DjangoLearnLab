# django-models/relationship_app/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.generic import DetailView
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from .models import UserProfile

# auth helpers
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import user_passes_test, login_required


# ---- existing views ----

def list_books(request):
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})


def list_books_text(request):
    books = Book.objects.all()
    if not books:
        return HttpResponse("No books available.", content_type="text/plain")
    lines = [f"{b.title} by {b.author.name}" for b in books]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def library_detail(request, library_name):
    library = Library.objects.get(name=library_name)
    books = library.books.select_related('author').all()
    return render(request, 'relationship_app/library_detail.html', {'library': library, 'books': books})


class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.select_related('author').all()
        return context


# ---- Authentication views (login/logout/register) ----

class AppLoginView(LoginView):
    template_name = 'relationship_app/login.html'


class AppLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('relationship_app:list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# -------------------------
# Role-based access helpers
# -------------------------

def _has_role(user, role_name):
    """
    Helper: return True if user has a profile with role == role_name.
    Gracefully handles missing profile.
    """
    if not user or not user.is_authenticated:
        return False
    # try to access related userprofile
    try:
        return user.userprofile.role == role_name
    except Exception:
        return False


# -------------------------
# Role-based views (names required)
# -------------------------

@user_passes_test(lambda u: _has_role(u, UserProfile.ROLE_ADMIN))
def admin_view(request):
    """
    View visible only to Admin users.
    """
    return render(request, 'relationship_app/admin_view.html', {'user': request.user})


@user_passes_test(lambda u: _has_role(u, UserProfile.ROLE_LIBRARIAN))
def librarian_view(request):
    """
    View visible only to Librarian users.
    """
    return render(request, 'relationship_app/librarian_view.html', {'user': request.user})


@user_passes_test(lambda u: _has_role(u, UserProfile.ROLE_MEMBER))
def member_view(request):
    """
    View visible only to Member users.
    """
    return render(request, 'relationship_app/member_view.html', {'user': request.user})
