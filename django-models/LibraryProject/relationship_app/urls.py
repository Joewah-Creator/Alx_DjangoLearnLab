# relationship_app/urls.py
from django.urls import path
from . import views

app_name = 'relationship_app'

urlpatterns = [
    # function-based view (plain text list of book titles and authors)
    path('books/', views.list_books, name='list_books'),

    # class-based detail view showing a specific library (by pk)
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),
]
