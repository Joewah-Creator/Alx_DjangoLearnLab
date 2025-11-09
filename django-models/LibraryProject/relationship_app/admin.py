from django.contrib import admin
from .models import Book, Library, Author

admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Author)

