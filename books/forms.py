from django import forms
from .models import Book, Genre, Author
from taggit.forms import TagField


class CreateBookForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={"size": "10"}))
    genre = forms.ModelChoiceField(Genre.objects.all())
    author = forms.ModelChoiceField(Author.objects.all())
    tags = TagField()

    class Meta:
        model = Book
        fields = ["title", "description", "image", "genre", "author", "tags"]


class UpdateBookForm(forms.ModelForm):
    tags = TagField()

    class Meta:
        model = Book
        fields = ["title", "description", "tags"]
