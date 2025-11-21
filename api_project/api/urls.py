# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from .views import BookList, BookViewSet

router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Existing ListAPIView
    path('books/', BookList.as_view(), name='book-list'),

    # Token authentication endpoint
    path('token/', obtain_auth_token, name='api-token'),

    # All router-based CRUD routes
    path('', include(router.urls)),
]

