from django import forms
from .models import Book, Note, Quote

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'cover', 'status', 'total_pages', 'current_page', 'book_file']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'bm-input',
                'placeholder': 'e.g. The Name of the Wind',
            }),
            'author': forms.TextInput(attrs={
                'class': 'bm-input',
                'placeholder': 'e.g. Patrick Rothfuss',
            }),
            'cover': forms.ClearableFileInput(attrs={
                'class': 'bm-input-file',
                'accept': 'image/*',
            }),
            'status': forms.Select(attrs={
                'class': 'bm-select',
            }),
            'total_pages': forms.NumberInput(attrs={
                'class': 'bm-input',
                'placeholder': '0',
                'min': '1',
            }),
            'current_page': forms.NumberInput(attrs={
                'class': 'bm-input',
                'placeholder': '0',
                'min': '0',
            }),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        exclude = ['book']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'bm-input',
                'placeholder': 'e.g. Chapter 5 thoughts…',
            }),
            'content': forms.Textarea(attrs={
                'class': 'bm-textarea',
                'rows': 6,
                'placeholder': 'Write your thoughts, observations, or anything worth remembering…',
            }),
        }


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        exclude = ['book']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'bm-textarea',
                'rows': 5,
                'placeholder': 'Type the quote exactly as it appears in the book…',
            }),
        }
