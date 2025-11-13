
from relationship_app.models import Author, Book, Library, Librarian

def create_sample_data():
    """
    Create sample data only if not present to make queries demonstrable.
    """
    # Create an author and books if they don't exist
    author, _ = Author.objects.get_or_create(name="Jane Doe")

    # Create books for this author
    b1, _ = Book.objects.get_or_create(title="Django Deep Dive", author=author)
    b2, _ = Book.objects.get_or_create(title="Advanced ORM Patterns", author=author)

    # Create a library and add books
    library, _ = Library.objects.get_or_create(name="Central Library")
    # Add books to library if they're not already added
    library.books.add(b1, b2)

    # Create a librarian for this library (OneToOne)
    # If a Librarian already exists for the library, skip creating duplicate
    if not hasattr(library, "librarian"):
        Librarian.objects.create(name="Sam Libris", library=library)

    # Additional library with other book to show many-to-many behavior
    other_author, _ = Author.objects.get_or_create(name="John Smith")
    other_book, _ = Book.objects.get_or_create(title="Pythonic Patterns", author=other_author)
    branch, _ = Library.objects.get_or_create(name="Branch Library")
    branch.books.add(other_book, b1)  # b1 present in both libraries

    return {
        "author": author,
        "books": [b1, b2],
        "library": library,
        "librarian": getattr(library, "librarian", None),
        "branch": branch,
        "other_book": other_book
    }

def query_books_by_author(author_name):
    """Query all books by a specific author."""
    try:
        author = Author.objects.get(name=author_name)
    except Author.DoesNotExist:
        print(f"No author found with name '{author_name}'")
        return []

    books = author.books.all()  # related_name='books' on Book.author
    print(f"Books by {author.name}:")
    for b in books:
        print(f" - {b.title}")
    return list(books)

def list_all_books_in_library(library_name):
    """List all books in a library."""
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")
        return []

    books = library.books.all()
    print(f"Books in {library.name}:")
    for b in books:
        print(f" - {b.title} (Author: {b.author.name})")
    return list(books)

def retrieve_librarian_for_library(library_name):
    """Retrieve the librarian for a library."""
    try:
        library = Library.objects.get(name=library_name)
    except Library.DoesNotExist:
        print(f"No library found with name '{library_name}'")
        return None

    # Using the related_name 'librarian' on the OneToOneField:
    try:
        librarian = library.librarian
        print(f"Librarian for {library.name}: {librarian.name}")
        return librarian
    except Librarian.DoesNotExist:
        print(f"No librarian assigned to {library.name}")
        return None
    except AttributeError:
        # If relationship wasn't set up or name collision
        print(f"No librarian attribute for {library.name}")
        return None

if __name__ == "__main__":
    # If accidentally run directly (not piped into manage.py shell), warn user.
    print("This script is intended to be run with the Django shell, for example:")
    print("  python manage.py shell < relationship_app/query_samples.py")
else:
    # If executed inside the Django shell via: python manage.py shell < relationship_app/query_samples.py
    data = create_sample_data()
    print("\n--- Sample data created/ensured ---\n")

    # 1) Query all books by a specific author
    query_books_by_author("Jane Doe")

    # 2) List all books in a library
    list_all_books_in_library("Central Library")

    # 3) Retrieve the librarian for a library
    retrieve_librarian_for_library("Central Library")
