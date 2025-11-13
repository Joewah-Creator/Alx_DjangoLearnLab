# django-models/relationship_app/urls.py

from django.urls import path
from .views import list_books
from .views import LibraryDetailView, library_detail

from . import views

app_name = 'relationship_app'

urlpatterns = [
    # function-based view for listing all books
    path('books/', list_books, name='list_books'),

    # class-based view for library by pk
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # function-based view by name (optional but already implemented)
    path('library/name/<str:library_name>/', library_detail, name='library_detail_by_name'),
]


