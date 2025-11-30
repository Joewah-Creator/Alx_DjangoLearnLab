from rest_framework import serializers
from .models import Author, Book
import datetime

# ---------------------------------------------------------------------
# BookSerializer
# Serializes all fields of Book.
# Adds custom validation to ensure publication_year is not in the future.
# ---------------------------------------------------------------------
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        read_only_fields = ['id']

    def validate_publication_year(self, value):
        """
        Ensure the publication_year is not in the future.
        Raises a ValidationError if the year is greater than the current year.
        """
        current_year = datetime.date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year cannot be in the future (current year is {current_year})."
            )
        return value

# ---------------------------------------------------------------------
# AuthorSerializer
# Serializes Author.name and includes a nested list of the author's books.
# The nested book list uses the BookSerializer to present book fields.
# We set `many=True` and `read_only=True` for the nested field since
# creation of nested books can be handled separately (keeps example simple).
# ---------------------------------------------------------------------
class AuthorSerializer(serializers.ModelSerializer):
    books = BookSerializer(many=True, read_only=True)  # maps to Author.books via related_name

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        read_only_fields = ['id']
