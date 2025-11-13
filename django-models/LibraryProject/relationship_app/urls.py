# django-models/relationship_app/urls.py

from django.urls import path
from .views import list_books
from .views import LibraryDetailView, library_detail
from .views import AppLoginView, AppLogoutView, register

app_name = 'relationship_app'

urlpatterns = [
    # books listing
    path('books/', list_books, name='list_books'),

    # class-based library detail by pk
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # function-based library detail by name
    path('library/name/<str:library_name>/', library_detail, name='library_detail_by_name'),

    # authentication URLs
    path('login/', AppLoginView.as_view(), name='login'),
    path('logout/', AppLogoutView.as_view(), name='logout'),
    path('register/', register, name='register'),
]



