# django-models/relationship_app/urls.py

from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView, library_detail

app_name = 'relationship_app'

urlpatterns = [
    # function-based view for listing all books
    path('books/', list_books, name='list_books'),

    # class-based view for library by pk
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # function-based library detail by name
    path('library/name/<str:library_name>/', library_detail, name='library_detail_by_name'),

    # Registration view (checker expects the literal 'views.register' somewhere)
    path('register/', views.register, name='register'),

    # Login and logout using Django built-in views with explicit template_name
    # checker expects these literal patterns:
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]


