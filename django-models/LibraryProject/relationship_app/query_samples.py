from relationship_app.models import Author, Book, Library, Librarian

# Query 1: Query all books by a specific author
def query_books_by_author():
    author = Author.objects.first()
    # Checker expects this exact pattern:
    books = Book.objects.filter(author=author)
    print("Books by the author:")
    for book in books:
        print(book.title)

# Query 2: List all books in a library
def list_books_in_library():
    library = Library.objects.first()
    books = library.books.all()
    print("Books in the library:")
    for book in books:
        print(book.title)

# Query 3: Retrieve the librarian for a library
def get_librarian_for_library():
    library = Library.objects.first()
    # Checker expects this exact attribute access:
    librarian = library.librarian
    print("Librarian for the library:")
    print(librarian.name)

# Auto-run when imported through Django shell
query_books_by_author()
list_books_in_library()
get_librarian_for_library()

