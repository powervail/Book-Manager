from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Note, Quote
from .forms import BookForm, NoteForm, QuoteForm
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Sum

# Create your views here.

def home(request):
    return render(request, 'books/home.html')

def book_list(request):
    books = Book.objects.all()

    query = request.GET.get('q')
    status = request.GET.get('status')

    if query:
        books = books.filter(Q(title__icontains=query) | Q(author__icontains=query))

    if status:
        books = books.filter(status=status)

    paginator = Paginator(books, 10)
    page_number = request.GET.get("page")
    books = paginator.get_page(page_number)


    return render(request, 'books/book_list.html', {"books": books})

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'books/book_detail.html', {"book": book})

def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', pk=book.pk)

    else:
        form = BookForm()
    return render(request, "books/book_form.html", {
        "form": form,
        "page_title": "Add Book",
        "button_text": "Add Book",
    })

def update_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form= BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)
    return render(request, "books/book_form.html", {
        "form": form,
        "page_title": "Edit Book",
        "button_text": "Save Changes",
    })

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        book.delete()
        return redirect("book_list")

    return render(request, "books/book_confirm_delete.html", {
        "book": book
    })

def create_note(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.book = book
            note.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = NoteForm()
    return render(request, "books/note_form.html", {"form":form})

def update_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST,instance=note)
        if form.is_valid():
            note = form.save()
            return redirect('book_detail', pk=note.book.pk) 
    else:
        form = NoteForm(instance=note)
    return render(request, 'books/note_form.html', {'form': form, 'note': note})

def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        book_id = note.book.pk
        note.delete()
        return redirect('book_detail', pk=book_id)
    return render(request, 'books/note_confirm_delete.html', {'note': note})

def create_quote(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.book = book
            quote.save()
            return redirect('book_detail', pk=book.pk)
    else:
        form = QuoteForm()
    return render(request, "books/quote_form.html", {'form': form})

def update_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    if request.method == "POST":
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            quote = form.save()
            return redirect('book_detail', pk=quote.book.pk)
        
    else:
        form = QuoteForm(instance=quote)
    return render(request, 'books/quote_form.html', {'form': form, 'quote': quote})

def delete_quote(request, pk):
    quote = get_object_or_404(Quote, pk=pk)
    if request.method == "POST":
        book_id = quote.book.pk
        quote.delete()
        return redirect('book_detail', pk=book_id)
    return render(request, 'books/quote_confirm_delete.html', {'quote': quote})


def dashboard(request):
    total_books = Book.objects.count()

    reading = Book.objects.filter(status='RD').count()
    completed = Book.objects.filter(status='CP').count()
    to_read = Book.objects.filter(status='NS').count()

    total_notes = Note.objects.count()
    total_quotes = Quote.objects.count()

    favorite_books = Book.objects.filter(is_favorite=True).count()

    total_pages = Book.objects.aggregate(total=Sum('total_pages'))["total"] or ()
    pages_read = Book.objects.aggregate(total=Sum('current_page'))["total"] or ()

    if total_pages:
        reading_precentage = (pages_read / total_pages) * 100
    else:
        reading_precentage = 0

    context = {
        "total_books": total_books,
        "reading": reading,
        "completed": completed,
        "to_read": to_read,
        "total_notes": total_notes,
        "total_quotes": total_quotes,
        "favorite_books": favorite_books,
        "total_pages": total_pages,
        "pages_read": pages_read,
        "reading_percentage": reading_precentage,
    }
    return render(request, "books/dashboard.html", context)

def toggle_favorite(request, pk):
    book = get_object_or_404(Book, pk=pk)

    book.is_favorite = not book.is_favorite
    book.save()

    return redirect('book_detail', pk=book.pk)

