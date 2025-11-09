from .models import Author, Book, Library, Librarian


def books_by_author(author_name):
    return Book.objects.filter(author__name=author_name)


def books_in_library(library_name):
    return Book.objects.filter(library__name=library_name)


def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)

