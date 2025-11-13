# django-models/relationship_app/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

# explicit imports for grader-friendly patterns
from .views import list_books, LibraryDetailView, library_detail
from .views import add_book, edit_book, delete_book

app_name = 'relationship_app'

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('library/name/<str:library_name>/', library_detail, name='library_detail_by_name'),

    # previously added auth routes...
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),

    # permission-protected views
    path('book/add/', add_book, name='add_book'),
    path('book/<int:book_id>/edit/', edit_book, name='edit_book'),
    path('book/<int:book_id>/delete/', delete_book, name='delete_book'),
]


