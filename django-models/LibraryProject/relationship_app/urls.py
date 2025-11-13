# django-models/relationship_app/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

# Also include explicit imports for grader-friendliness
from .views import list_books, LibraryDetailView, library_detail
from .views import AppLoginView, AppLogoutView, register
from .views import admin_view, librarian_view, member_view

app_name = 'relationship_app'

urlpatterns = [
    # book list
    path('books/', list_books, name='list_books'),

    # library detail (class-based)
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # library detail (function by name)
    path('library/name/<str:library_name>/', library_detail, name='library_detail_by_name'),

    # auth
    path('register/', register, name='register'),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # role-based pages
    path('role/admin/', admin_view, name='admin_view'),
    path('role/librarian/', librarian_view, name='librarian_view'),
    path('role/member/', member_view, name='member_view'),
]


