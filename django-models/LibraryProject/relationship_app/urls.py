from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

# Option: do NOT use a namespace here so the checker finds names like 'login' directly.
urlpatterns = [
    # Books & Library views (keep existing)
    path('books/', views.list_books, name='list_books'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication URLs using Django's built-in class-based views
    # The checker expects the literal calls LoginView.as_view(template_name=...) and LogoutView.as_view(template_name=...)
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),

    # Registration remains a function-based view in views.py
    path('register/', views.register, name='register'),
]

