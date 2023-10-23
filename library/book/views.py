from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from authentication.views import is_admin
from .models import Book
from library.forms import BookCreationForm

from rest_framework import viewsets
from .models import Book
from .serializers import BookSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


def concrete_book(request, book_id):
    book = Book.get_by_id(book_id)
    data = {
        'title': 'Books',
        'book': book,
        'user': request.user,
    }
    return render(request, 'book/book.html', data)


@login_required
@user_passes_test(is_admin)
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


@login_required
@user_passes_test(is_admin)
def delete_book(request, book_id):
    Book.delete_by_id(book_id)
    return redirect('home')
