from django.shortcuts import render, redirect
from .models import Book
from library.forms import BookCreationForm


def concrete_book(request, book_id):
    book = Book.get_by_id(book_id)
    data = {
        'title': 'Books',
        'book': book,
        'user': request.user,
    }
    return render(request, 'book/book.html', data)

def create_book(request, book_id=0):
    if request.method == 'POST':
        if book_id == 0:
            form = BookCreationForm(request.POST)
        else:
            book = Book.get_by_id(book_id)
            form = BookCreationForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        if book_id == 0:
            form = BookCreationForm()
        else:
            book = Book.get_by_id(book_id)
            form = BookCreationForm(instance=book)
    data = {
        'title': 'Create/edit book',
        'user': request.user,
        'form': form,
    }
    return render(request, 'book/create.html', data)
