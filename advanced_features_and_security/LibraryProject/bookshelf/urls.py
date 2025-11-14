from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.protected_list_books, name='protected_list_books'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:book_id>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:book_id>/delete/', views.delete_book, name='delete_book'),
]
