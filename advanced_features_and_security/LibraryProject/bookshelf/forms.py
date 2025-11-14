from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        if year is None:
            return 0
        if year < 0 or year > 9999:
            raise forms.ValidationError("Invalid publication year.")
        return year
