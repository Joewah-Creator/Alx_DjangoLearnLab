# django-models/relationship_app/urls.py

from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # function-based view listing all books
    path('books/', views.list_books, name='list_books'),

    # class-based view showing library details; expects pk
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]

