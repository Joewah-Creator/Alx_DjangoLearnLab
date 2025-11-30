# api/urls.py
from django.urls import path
from . import generic_views

urlpatterns = [
    # List & detail (read)
    path('books/', generic_views.BookListAPIView.as_view(), name='book-list'),
    path('books/<int:pk>/', generic_views.BookDetailAPIView.as_view(), name='book-detail'),

    # Create, update, delete (mutating - require auth)
    path('books/create/', generic_views.BookCreateAPIView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', generic_views.BookUpdateAPIView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', generic_views.BookDeleteAPIView.as_view(), name='book-delete'),
]
