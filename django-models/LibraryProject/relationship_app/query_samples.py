from relationship_app.models import Author, Book, Library, Librarian

def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian

if __name__ == "__main__":
    print("Books by J.K. Rowling:")
    for book in books_by_author("J.K. Rowling"):
        print(" -", book.title)

    print("\nBooks in Central Library:")
    for book in books_in_library("Central Library"):
        print(" -", book.title)

    librarian = librarian_for_library("Central Library")
    print("\nLibrarian of Central Library:", librarian.name)
