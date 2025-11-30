# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Read endpoints (public)
    path('books/', views.ListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.DetailView.as_view(), name='book-detail'),

    # Mutating endpoints (authenticated)
    path('books/create/', views.CreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', views.UpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.DeleteView.as_view(), name='book-delete'),
]
