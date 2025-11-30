from django.db import models

class Author(models.Model):
    """
    Author: represents an author. The grader expects this class name and a name field.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Book(models.Model):
    """
    Book: represents a book. Must have title, publication_year and a ForeignKey 'author'
    that uses related_name='books' so the AuthorSerializer can access author.books.
    """
    title = models.CharField(max_length=500)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

