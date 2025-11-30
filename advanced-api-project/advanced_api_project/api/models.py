from django.db import models

# ---------------------------------------------------------------------
# Author model
# Purpose: Represents an author who may have multiple books.
# Fields:
#   - name: CharField storing the author's name.
# ---------------------------------------------------------------------
class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# ---------------------------------------------------------------------
# Book model
# Purpose: Represents a book written by an Author.
# Fields:
#   - title: Title of the book.
#   - publication_year: Integer year the book was published.
#   - author: ForeignKey relation to Author (one-to-many).
# Notes:
#   - related_name='books' allows easy reverse access: author.books.all()
# ---------------------------------------------------------------------
class Book(models.Model):
    title = models.CharField(max_length=500)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

